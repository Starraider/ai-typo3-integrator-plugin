#!/usr/bin/env php
<?php

declare(strict_types=1);

function usage(): void
{
    fwrite(STDOUT, <<<'TXT'
Usage: inspect-deployer.php [--project-root PATH] [--format text|json]

Read composer.json, composer.lock, the local Deployer binary, and root-level
Deployer recipes. The script does not modify files or contact a server.

Exit codes:
  0  inspection completed
  2  invalid arguments or missing project files
  3  malformed JSON or unreadable input
TXT);
    fwrite(STDOUT, PHP_EOL);
}

function fail(string $message, int $code): never
{
    fwrite(STDERR, "inspect-deployer: {$message}" . PHP_EOL);
    exit($code);
}

function readJsonFile(string $path): array
{
    $contents = @file_get_contents($path);
    if ($contents === false) {
        fail("cannot read {$path}", 3);
    }

    try {
        $decoded = json_decode($contents, true, 512, JSON_THROW_ON_ERROR);
    } catch (JsonException $exception) {
        fail("invalid JSON in {$path}: {$exception->getMessage()}", 3);
    }

    if (!is_array($decoded)) {
        fail("expected a JSON object in {$path}", 3);
    }

    return $decoded;
}

function majorFromVersion(?string $version): ?int
{
    if ($version === null) {
        return null;
    }

    if (preg_match('/(?:^|\s|v)(\d+)\./i', $version, $matches) === 1) {
        return (int) $matches[1];
    }

    return null;
}

function majorsFromConstraint(?string $constraint): array
{
    if ($constraint === null) {
        return [];
    }

    preg_match_all('/(?<!\d)(?:v)?([78])(?:\.\d+|\.x|\.\*)?/i', $constraint, $matches);
    $majors = array_map('intval', $matches[1] ?? []);
    $majors = array_values(array_unique($majors));
    sort($majors);

    return $majors;
}

function findLockedVersion(array $lock): ?string
{
    foreach (['packages', 'packages-dev'] as $section) {
        foreach ($lock[$section] ?? [] as $package) {
            if (($package['name'] ?? null) === 'deployer/deployer') {
                return is_string($package['version'] ?? null) ? $package['version'] : null;
            }
        }
    }

    return null;
}

function scanRecipe(string $path): array
{
    $patterns = [
        [
            'id' => 'run-options-array',
            'severity' => 'high',
            'regex' => '/\b(?:run|runLocally)\s*\([^;\n]*,\s*\[/',
            'message' => 'Review a possible v7 run or runLocally options array and convert options to named arguments.',
        ],
        [
            'id' => 'renamed-run-option',
            'severity' => 'high',
            'regex' => '/\b(?:no_throw|real_time_output|idle_timeout)\b/',
            'message' => 'Migrate renamed Deployer 8 run parameters: nothrow, forceOutput, or idleTimeout.',
        ],
        [
            'id' => 'single-secret-argument',
            'severity' => 'high',
            'regex' => '/\bsecret\s*:/',
            'message' => 'Replace the v7 secret argument with the v8 secrets map and named placeholders.',
        ],
        [
            'id' => 'single-secret-placeholder',
            'severity' => 'high',
            'regex' => '/%secret%/',
            'message' => 'Replace %secret% with a name from the v8 secrets map.',
        ],
        [
            'id' => 'php-shell-escape',
            'severity' => 'high',
            'regex' => '/\bescapeshellarg\s*\(/',
            'message' => 'Use Deployer quote() for command arguments under v8.',
        ],
        [
            'id' => 'httpie-get-json',
            'severity' => 'high',
            'regex' => '/\bHttpie::getJson\s*\(/',
            'message' => 'Replace deprecated Httpie::getJson() with sendJson().',
        ],
        [
            'id' => 'typo3-webroot-v7',
            'severity' => 'high',
            'regex' => '/[\'\"]typo3_webroot[\'\"]/',
            'message' => 'Replace the v7 TYPO3 webroot setting with typo3/public_dir when an override is needed.',
        ],
        [
            'id' => 'legacy-path-setting',
            'severity' => 'info',
            'regex' => '/[\'\"](?:web_path|public_path)[\'\"]/',
            'message' => 'Find the reader of this path setting and remove it only if the v8 project no longer uses it.',
        ],
        [
            'id' => 'empty-typo3-path-override',
            'severity' => 'info',
            'regex' => '/\bset\s*\(\s*[\'\"](?:shared_dirs|writable_dirs)[\'\"]\s*,\s*\[\s*\]\s*\)/',
            'message' => 'An empty override disables TYPO3 recipe defaults. Compare it with the live shared layout.',
        ],
        [
            'id' => 'empty-typo3-path-addition',
            'severity' => 'info',
            'regex' => '/\badd\s*\(\s*[\'\"](?:shared_dirs|writable_dirs)[\'\"]\s*,\s*\[\s*\]\s*\)/',
            'message' => 'This empty addition is a no-op. Remove it after confirming that the recipe defaults should remain active.',
        ],
        [
            'id' => 'deployer-self-update',
            'severity' => 'high',
            'regex' => '/\b(?:self-update|selfupdate)\b/i',
            'message' => 'Deployer 8 removed self-update. Manage the project binary with Composer.',
        ],
    ];

    $lines = @file($path, FILE_IGNORE_NEW_LINES);
    if ($lines === false) {
        return [[
            'id' => 'unreadable-recipe',
            'severity' => 'high',
            'message' => "Cannot read recipe {$path}.",
            'lines' => [],
        ]];
    }

    $findings = [];
    foreach ($patterns as $pattern) {
        $matchedLines = [];
        foreach ($lines as $index => $line) {
            if (preg_match($pattern['regex'], $line) === 1) {
                $matchedLines[] = $index + 1;
            }
        }

        if ($matchedLines !== []) {
            $findings[] = [
                'id' => $pattern['id'],
                'severity' => $pattern['severity'],
                'message' => $pattern['message'],
                'lines' => $matchedLines,
            ];
        }
    }

    return $findings;
}

$projectRoot = getcwd() ?: '.';
$format = 'text';

for ($index = 1; $index < $argc; $index++) {
    $argument = $argv[$index];
    if ($argument === '--help' || $argument === '-h') {
        usage();
        exit(0);
    }
    if ($argument === '--project-root') {
        $projectRoot = $argv[++$index] ?? fail('--project-root requires a value', 2);
        continue;
    }
    if (str_starts_with($argument, '--project-root=')) {
        $projectRoot = substr($argument, strlen('--project-root='));
        continue;
    }
    if ($argument === '--format') {
        $format = $argv[++$index] ?? fail('--format requires a value', 2);
        continue;
    }
    if (str_starts_with($argument, '--format=')) {
        $format = substr($argument, strlen('--format='));
        continue;
    }
    fail("unknown argument {$argument}", 2);
}

if (!in_array($format, ['text', 'json'], true)) {
    fail('--format must be text or json', 2);
}

$resolvedRoot = realpath($projectRoot);
if ($resolvedRoot === false || !is_dir($resolvedRoot)) {
    fail("project root does not exist: {$projectRoot}", 2);
}

$composerPath = $resolvedRoot . '/composer.json';
if (!is_file($composerPath)) {
    fail("composer.json not found under {$resolvedRoot}", 2);
}

$composer = readJsonFile($composerPath);
$constraint = null;
$constraintSection = null;
foreach (['require-dev', 'require'] as $section) {
    if (isset($composer[$section]['deployer/deployer']) && is_string($composer[$section]['deployer/deployer'])) {
        $constraint = $composer[$section]['deployer/deployer'];
        $constraintSection = $section;
        break;
    }
}

$lockPath = $resolvedRoot . '/composer.lock';
$lockedVersion = is_file($lockPath) ? findLockedVersion(readJsonFile($lockPath)) : null;

$binaryPath = $resolvedRoot . '/vendor/bin/dep';
$binaryVersion = null;
if (is_file($binaryPath) && is_executable($binaryPath)) {
    $output = [];
    $exitCode = 0;
    exec(escapeshellarg($binaryPath) . ' --version 2>&1', $output, $exitCode);
    if ($exitCode === 0) {
        $binaryVersion = trim(implode("\n", $output));
    }
}

$majors = majorsFromConstraint($constraint);
foreach ([$lockedVersion, $binaryVersion] as $versionEvidence) {
    $major = majorFromVersion($versionEvidence);
    if ($major !== null) {
        $majors[] = $major;
    }
}
$majors = array_values(array_unique($majors));
sort($majors);

if ($constraint === null && $lockedVersion === null && $binaryVersion === null) {
    $state = 'absent';
} elseif ($majors === [7]) {
    $state = 'v7';
} elseif ($majors === [8]) {
    $state = 'v8';
} elseif (in_array(7, $majors, true) && in_array(8, $majors, true)) {
    $state = 'mixed';
} else {
    $state = 'unknown';
}

$recipePaths = [];
foreach (['deploy.php', 'deploy.yaml', 'deploy.yml', 'deploy.maml'] as $recipeName) {
    if (is_file($resolvedRoot . '/' . $recipeName)) {
        $recipePaths[] = $recipeName;
    }
}
foreach (glob($resolvedRoot . '/deploy*.php') ?: [] as $candidate) {
    $relative = basename($candidate);
    if (!in_array($relative, $recipePaths, true)) {
        $recipePaths[] = $relative;
    }
}
sort($recipePaths);

$findings = [];
foreach ($recipePaths as $relativePath) {
    foreach (scanRecipe($resolvedRoot . '/' . $relativePath) as $finding) {
        $finding['file'] = $relativePath;
        $findings[] = $finding;
    }
}

$highCount = count(array_filter($findings, static fn (array $finding): bool => $finding['severity'] === 'high'));
$infoCount = count($findings) - $highCount;

$report = [
    'project_root' => $resolvedRoot,
    'php' => [
        'version' => PHP_VERSION,
        'supports_deployer_8' => version_compare(PHP_VERSION, '8.3.0', '>='),
    ],
    'deployer' => [
        'state' => $state,
        'constraint' => $constraint,
        'constraint_section' => $constraintSection,
        'locked_version' => $lockedVersion,
        'binary_version' => $binaryVersion,
        'evidence_majors' => $majors,
    ],
    'recipes' => $recipePaths,
    'findings' => $findings,
    'summary' => [
        'high' => $highCount,
        'info' => $infoCount,
        'total' => count($findings),
    ],
];

if ($format === 'json') {
    fwrite(STDOUT, json_encode($report, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_THROW_ON_ERROR) . PHP_EOL);
    exit(0);
}

fwrite(STDOUT, "Project: {$resolvedRoot}" . PHP_EOL);
fwrite(STDOUT, "PHP: " . PHP_VERSION . ($report['php']['supports_deployer_8'] ? ' (v8 compatible)' : ' (v8 requires PHP 8.3+)') . PHP_EOL);
fwrite(STDOUT, "Deployer state: {$state}" . PHP_EOL);
fwrite(STDOUT, "Constraint: " . ($constraint ?? 'none') . ($constraintSection !== null ? " in {$constraintSection}" : '') . PHP_EOL);
fwrite(STDOUT, "Locked: " . ($lockedVersion ?? 'none') . PHP_EOL);
fwrite(STDOUT, "Binary: " . ($binaryVersion ?? 'none') . PHP_EOL);
fwrite(STDOUT, "Recipes: " . ($recipePaths === [] ? 'none' : implode(', ', $recipePaths)) . PHP_EOL);
fwrite(STDOUT, "Findings: {$highCount} high, {$infoCount} info" . PHP_EOL);
foreach ($findings as $finding) {
    $lineList = implode(',', $finding['lines']);
    fwrite(STDOUT, sprintf(
        "- [%s] %s:%s %s (%s)\n",
        $finding['severity'],
        $finding['file'],
        $lineList,
        $finding['message'],
        $finding['id'],
    ));
}
