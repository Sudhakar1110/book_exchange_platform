$reports_ws = "book_exchange\book_exchange_platform\workspace\reports\reports.json"
$main_ws = "book_exchange\book_exchange_platform\workspace\book_exchange_platform\book_exchange_platform.json"

function Update-Workspace {
    param([string]$FilePath)
    if (-not (Test-Path $FilePath)) { return }
    $json = Get-Content -Raw -Path $FilePath | ConvertFrom-Json

    # Check if already exists
    foreach ($link in $json.links) {
        if ($link.link_to -eq "Member Activity Report") { return }
    }

    # Add link
    $newLink = @{
        hidden = 0
        is_query_report = 1
        label = "Member Activity Report"
        link_count = 0
        link_to = "Member Activity Report"
        link_type = "Report"
        onboard = 0
        type = "Link"
    }
    $json.links += $newLink

    # Add shortcut
    $newShortcut = @{
        color = "Gray"
        doc_view = ""
        label = "Member Activity Report"
        link_to = "Member Activity Report"
        type = "Report"
    }
    $json.shortcuts += $newShortcut

    # Add content
    $contentArray = $json.content | ConvertFrom-Json
    $newContent = @{
        id = "member_activity_report"
        type = "shortcut"
        data = @{
            shortcut_name = "Member Activity Report"
            col = 3
        }
    }
    $contentArray += $newContent
    $json.content = ConvertTo-Json $contentArray -Depth 10 -Compress

    # Save
    $json | ConvertTo-Json -Depth 100 | Set-Content -Path $FilePath
}

Update-Workspace $reports_ws
Update-Workspace $main_ws
