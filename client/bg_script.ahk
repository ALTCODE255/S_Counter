#Requires AutoHotkey v2.0.11+

:B0X?*:sonic::updateCount("Sonic")
:B0X?*:shuuen::updateCount("Shuuen")

!1::updateCount("Sonic")
!2::updateCount("Shuuen")

URL := IniRead("vars.ini", "HTTP", "URL")
AUTH := IniRead("vars.ini", "HTTP", "HEADER_AUTH")

updateCount(col) {
    req := ComObject('WinHttp.WinHttpRequest.5.1')
    req.Open("POST", URL "/increment")
    req.SetRequestHeader("Authorization", AUTH)
    req.SetRequestHeader("inc-col", col)
    req.Option[4] := "&H3300"
    req.Send()
    req.WaitForResponse()
    TrayTip col ": " req.ResponseText
}