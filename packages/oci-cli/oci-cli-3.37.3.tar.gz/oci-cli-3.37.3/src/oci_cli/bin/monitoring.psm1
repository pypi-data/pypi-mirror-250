function GetOciTopLevelCommand_monitoring() {
    return 'monitoring'
}

function GetOciSubcommands_monitoring() {
    $ociSubcommands = @{
        'monitoring' = 'alarm alarm-dimension-states-collection alarm-history-collection alarm-status metric metric-data suppression'
        'monitoring alarm' = 'change-compartment create delete get list update'
        'monitoring alarm-dimension-states-collection' = 'retrieve-dimension-states'
        'monitoring alarm-history-collection' = 'get-alarm-history'
        'monitoring alarm-status' = 'list-alarms-status'
        'monitoring metric' = 'list'
        'monitoring metric-data' = 'post summarize-metrics-data'
        'monitoring suppression' = 'remove'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_monitoring() {
    $ociCommandsToLongParams = @{
        'monitoring alarm change-compartment' = 'alarm-id compartment-id from-json help if-match'
        'monitoring alarm create' = 'body compartment-id defined-tags destinations display-name freeform-tags from-json help is-enabled is-notifications-per-metric-dimension-enabled max-wait-seconds message-format metric-compartment-id metric-compartment-id-in-subtree namespace pending-duration query-text repeat-notification-duration resolution resource-group severity suppression wait-for-state wait-interval-seconds'
        'monitoring alarm delete' = 'alarm-id force from-json help if-match max-wait-seconds wait-for-state wait-interval-seconds'
        'monitoring alarm get' = 'alarm-id from-json help'
        'monitoring alarm list' = 'all compartment-id compartment-id-in-subtree display-name from-json help lifecycle-state limit page page-size sort-by sort-order'
        'monitoring alarm update' = 'alarm-id body compartment-id defined-tags destinations display-name force freeform-tags from-json help if-match is-enabled is-notifications-per-metric-dimension-enabled max-wait-seconds message-format metric-compartment-id metric-compartment-id-in-subtree namespace pending-duration query-text repeat-notification-duration resolution resource-group severity suppression wait-for-state wait-interval-seconds'
        'monitoring alarm-dimension-states-collection retrieve-dimension-states' = 'alarm-id dimension-filters from-json help limit page status'
        'monitoring alarm-history-collection get-alarm-history' = 'alarm-historytype alarm-id from-json help limit page timestamp-greater-than-or-equal-to timestamp-less-than'
        'monitoring alarm-status list-alarms-status' = 'all compartment-id compartment-id-in-subtree display-name entity-id from-json help limit page page-size resource-id service-name sort-by sort-order status'
        'monitoring metric list' = 'all compartment-id compartment-id-in-subtree dimension-filters from-json group-by help limit name namespace page page-size resource-group sort-by sort-order'
        'monitoring metric-data post' = 'batch-atomicity content-encoding from-json help metric-data'
        'monitoring metric-data summarize-metrics-data' = 'compartment-id compartment-id-in-subtree end-time from-json help namespace query-text resolution resource-group start-time'
        'monitoring suppression remove' = 'alarm-id from-json help if-match'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_monitoring() {
    $ociCommandsToShortParams = @{
        'monitoring alarm change-compartment' = '? c h'
        'monitoring alarm create' = '? c h'
        'monitoring alarm delete' = '? h'
        'monitoring alarm get' = '? h'
        'monitoring alarm list' = '? c h'
        'monitoring alarm update' = '? c h'
        'monitoring alarm-dimension-states-collection retrieve-dimension-states' = '? h'
        'monitoring alarm-history-collection get-alarm-history' = '? h'
        'monitoring alarm-status list-alarms-status' = '? c h'
        'monitoring metric list' = '? c h'
        'monitoring metric-data post' = '? h'
        'monitoring metric-data summarize-metrics-data' = '? c h'
        'monitoring suppression remove' = '? h'
    }
    return $ociCommandsToShortParams
}