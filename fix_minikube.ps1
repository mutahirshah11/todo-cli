$path = 'C:\Users\DELL\.minikube'
Get-ChildItem -Path $path -Recurse -Force -ErrorAction SilentlyContinue | ForEach-Object {
    try { $_.Attributes = 'Normal' } catch {}
}
Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
if (Test-Path $path) {
    Write-Host "STILL EXISTS - trying robocopy trick"
    $empty = New-Item -ItemType Directory -Path "$env:TEMP\empty_dir" -Force
    robocopy "$empty" "$path" /MIR /NFL /NDL /NJH /NJS | Out-Null
    Remove-Item $path -Recurse -Force
    Remove-Item $empty -Recurse -Force
}
Write-Host "Done. minikube dir exists: $(Test-Path $path)"
