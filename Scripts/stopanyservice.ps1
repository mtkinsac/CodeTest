function stopAnyService{
    param(
        [string]$serviceName,
        [string]$computerName=$env:computername
        )
     
    function executeKillCommand($serviceName){
 
        write-host "including prerequisites..."
        .{
            # Prerequisite commands
            $chocoAvailable="get-command choco -ErrorAction SilentlyContinue";
            $psexecAvailable="get-command psexec -ErrorAction SilentlyContinue";
            $setAclAvailable="get-command setacl -ErrorAction SilentlyContinue";
 
            if (!(Invoke-Expression $chocoAvailable)) {
                write-host "Installing Choco...";
                Set-ExecutionPolicy Bypass -Scope Process -Force;
                iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'));
                }
            if (!(Invoke-Expression $chocoAvailable)) {
                write-host "Unable to install Chocolatey automation tool. Program now aborts.";
                break;
                }
             
            if(!(Invoke-Expression $psexecAvailable)){
 
                $pendingRebootTests = @(
                    @{
                        Name = 'RebootPending'
                        Test = { Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing' -Name 'RebootPending' -ErrorAction SilentlyContinue }
                        TestType = 'ValueExists'
                    }
                    @{
                        Name = 'RebootRequired'
                        Test = { Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update' -Name 'RebootRequired' -ErrorAction SilentlyContinue }
                        TestType = 'ValueExists'
                    }
                    @{
                        Name = 'PendingFileRenameOperations'
                        Test = { Get-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager' -Name 'PendingFileRenameOperations' -ErrorAction SilentlyContinue }
                        TestType = 'NonNullValue'
                    }
                )
                foreach ($test in $pendingRebootTests) {
                    $pendingReboot=Invoke-Command -ScriptBlock $test.Test
                    if($pendingReboot){
                        write-host "$env:computername currently has a pending reboot requirement. Aborting session...";
                        break;
                        }
                }
 
                try { 
                    $status = ([wmiclass]"\\.\root\ccm\clientsdk:CCM_ClientUtilities").DetermineIfRebootPending()
                    if(($status -ne $null) -and $status.RebootPending){
                        write-host "$env:computername currently has a pending reboot requirement. Aborting session...";
                        break;
                        }
                    }catch{}
 
                write-host "Installing PSExec...";
                choco install sysinternals -y -force;
                }
            if (!(Invoke-Expression $psexecAvailable)) {
                write-host "Unable to install psexec. Program now aborts.";
                break;
                }
 
            if(!(Invoke-Expression $setAclAvailable)){
                write-host "Installing setacl...";
                choco install setacl -y -force;
                }
             if (!(Invoke-Expression $setAclAvailable)) {
                write-host "Unable to install setACL. Program now aborts.";
                break;
                }                          
            write-host "Done.";
 
        }
 
        function forceKillService ($service){
        if ($service.Status -ne "Stopped"){
            # Try to stop the service as normal - only modify permissions and retry upon encountering errors
            try{
                Stop-Service $serviceName -Force -ErrorAction Stop;
                }
            catch{
                $serviceRunas=(Get-WMIObject win32_service |?{$_ -like "*$serviceName*"}).StartName;
 
                <# $serviceRunas=(Get-CIMInstance win32_service |?{$_ -like "*$serviceName*"}).StartName;
                The term 'Get-CIMInstance' is not recognized as the name of a cmdlet, function, script file, or operable program. Check
                 the spelling of the name, or if a path was included, verify that the path is correct and try again.
                At line:1 char:16
                + Get-CIMInstance <<<<  win32_service
                    + CategoryInfo          : ObjectNotFound: (Get-CIMInstance:String) [], CommandNotFoundException
                    + FullyQualifiedErrorId : CommandNotFoundException
                #>
 
                write-host "$serviceName seems to be owned by $serviceRunas. Now seizing permissions...";
 
                # Grant permissions of service to the Administrators group
                $nullOutput=PSExec -s SetACL.exe -on $serviceName -ot srv -actn ace -ace 'n:Administrators;p:full' 2>&1; #redirect (>) 'stderr'(2) messages to 'stdout'(1); where 1 is a file descriptor (&), not a file
                write-host "Process name $serviceName has been granted access to the Administrators group.";
 
                # Retry stopping service
                try{
                    Stop-Service $serviceName -Force;
                    write-host "$serviceName has been stopped successfully.";
                    return $true;
                    }
                catch{
                    write-host $Error;
                    write-host "$serviceName has NOT been stopped successfully.";
                    return $false;
                    }
                }
 
            }else{
                write-host "$serviceName is already stopped.";
                return $true;
                }
        }
         
        $matches=get-service|?{$_.DisplayName -like "*$serviceName*" -or $_.Name -like "*$serviceName*" -or $_.Servicename -like "*$serviceName*"};
        #$matches=get-service|?{$_.DisplayName -like "*$serviceName*" -or $_.Name -like "*$serviceName*"};
        if (!($matches)){
            $message="$serviceName doesn't match anything on $env:computername";
            write-host $message;
            return $false;
            }
         
        if($matches.count -gt 1){
            # This is a PowerShell 2.0 backward compatible technique to rebuild an object with a new column of Index values
            $displayMatches=for ($i=0;$i -lt $matches.count;$i++){
                $matches[$i]|Select-Object @{name='Index';e={$i}},Name,Displayname,Status
                }
            $displayMatches=$displayMatches|ft -AutoSize|Out-String
            write-host "We have multiple matches for the $servicename`:`r`n-----------------------------------------------------------------$displayMatches";
            $input=Read-Host "Please pick an index number from the above list"
            write-host "Index value $input received.";
            $matches=$matches[$input];
            if (!($matches)){
                write-host "Index value $input is invalid. No actions were taken.";
                return $false;
                }else{
                    $service=$matches;
                    forceKillService $service;
                    return $true;
                    }        
            }else{
                $service=$matches;         
                forceKillService $service;
                return $true;
                }
         
    }
 
    function initPsSessionAsAdmin($computerName){
        function checkAdminPrivileges{
            param($credential)
            $myWindowsID=[System.Security.Principal.WindowsIdentity]::GetCurrent()
            $currentUser=$myWindowsID.Name
            $myWindowsPrincipal=new-object System.Security.Principal.WindowsPrincipal($myWindowsID)
            $adminRole=[System.Security.Principal.WindowsBuiltInRole]::Administrator;
            if ($myWindowsPrincipal.IsInRole($adminRole))
               {
               write-host "$currentUser is an Administrator. Program will now initiate a new session with such account...";
               $Host.UI.RawUI.BackgroundColor = "Black";
               return $true;
               }
            else
               {
               return $false;
               }
 
            }
 
        function getAdminCredentials{
            $exitLoop=$false;
            do {
                $credential= get-credential;
                if(checkAdminPrivileges -credential $credential){$exitLoop=$true};
                sleep 1;
                }while ($exitLoop -eq $false)
            return $credential;
            }
 
        if (!(checkAdminPrivileges)){
            $cred=getAdminCredentials
            try{
                $session=New-PSSession -Credential $cred -ComputerName $computerName;
                }catch{
                    # Enable WinRM as try block command didn't succeed;
                    start-process powershell.exe -credential $cred -nonewwindow -ArgumentList "enable-psremoting -force";
                    refreshenv;
                    $session=New-PSSession -Credential $cred -ComputerName $computerName;
                    }
            }else{
                try{
                $session=New-PSSession -ComputerName $computerName;
                }catch{                    
                    # Enable WinRM as try block command didn't succeed;
                    start-process powershell.exe -credential $cred -nonewwindow -ArgumentList "winrm quickconfig -force;"
                    refreshenv;
                    $session=New-PSSession -ComputerName $computerName;
                    }                
                }
        if ($session){
            return $session;
            }else{
                write-host "Could not proceed due to errors in the process of initiating a new PSSession.";
                break;
                }
    }
 
    function invokeKillCommand{
        param($service)
 
        # Cleanup any lingering PS Sessions
        get-pssession|remove-pssession;
 
        if (!$adminPsSession -or $adminPsSession.State -eq "Closed"){$adminPsSession=initPsSessionAsAdmin -computerName $computerName;}       
 
        if(!(get-command psexec -ea SilentlyContinue)){
            if (!(get-command choco -ea SilentlyContinue)) {
                write-host "Installing Choco...";
                Set-ExecutionPolicy Bypass -Scope Process -Force;
                iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'));
                }
 
            write-host "Installing PSExec...";
            choco install sysinternals -y -force;
            }
 
        # Setting WinRM memory size to ensure success
        #Correct format: winrm set winrm/config/winrs '@{MaxMemoryPerShellMB="$ramMB"}'
        #Alternaltive: psexec \\$computerName PowerShell Set-Item WSMan:\localhost\Shell\MaxMemoryPerShellMB 1024 #This one runs into permission issues
        [int]$ramMB=(gwmi -Class win32_operatingsystem -computername $computerName -ea stop).TotalVisibleMemorySize/1024
        if ($ramMB -ge 4090){$ramMB=4090}
        $nullOutput=invoke-expression "psexec \\$computerName -s winrm.cmd set winrm/config/winrs '@{MaxMemoryPerShellMB=`"$ramMB`"}'" 2>&1;
 
        invoke-command -Session $adminPsSession -ScriptBlock{
            param($importedFunc,$x)
            [ScriptBlock]::Create($importedFunc).invoke($x); 
            } -args ${function:executeKillCommand},$service
        Remove-PSSession $adminPsSession;
    }
 
    function killService{
        param($service)
        $computerNameRegex='^(.*?)\.'
        $local=$([void]($computerName -match $computerNameRegex);if($matches){$matches[1]}else{$computerName}) -like $env:computername;
        if ($local){
            executeKillCommand -service $service;                    
            }else{
                invokeKillCommand -service $service;
                }
        }
    killService -service $serviceName
}
stopAnyService -serviceName "MsMpSvc" -computerName $env:computername