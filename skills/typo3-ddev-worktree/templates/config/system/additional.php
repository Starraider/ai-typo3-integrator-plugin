<?php
/**
 * Configuration snippet for TYPO3 config/system/additional.php
 * to support Vite dev server in DDEV worktrees and local environments.
 */

// Dynamic Vite dev server configuration for worktrees and local environments:
// If VITE_SERVER_URI is not explicitly provided in the environment,
// automatically derive https://vite.<project>.ddev.site from DDEV_HOSTNAME.
if (empty(getenv('VITE_SERVER_URI'))) {
    $ddevHostname = getenv('DDEV_HOSTNAME');
    if ($ddevHostname) {
        $primaryHost = explode(',', $ddevHostname)[0];
        $GLOBALS['TYPO3_CONF_VARS']['EXTENSIONS']['vite_asset_collector']['devServerUri'] = 'https://vite.' . $primaryHost;
    }
}

// Optional dev-server override toggle via environment variable:
// Allows testing compiled production assets (manifest.json) in Development context
// by setting TYPO3_USE_VITE_DEV_SERVER=0 in .env without changing TYPO3_CONTEXT.
if (getenv('TYPO3_USE_VITE_DEV_SERVER') !== false && getenv('TYPO3_USE_VITE_DEV_SERVER') !== '') {
    $GLOBALS['TYPO3_CONF_VARS']['EXTENSIONS']['vite_asset_collector']['useDevServer'] = (bool)getenv('TYPO3_USE_VITE_DEV_SERVER');
}
