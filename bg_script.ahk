SetWorkingDir %A_ScriptDir%

increment(str)
{
    Run, pythonw increment.pyw %str%
    return
}

:B0X:sonic::increment("Sonic")

:B0X:shuuen::increment("Shuuen")

!1::increment("Sonic")

!2::increment("Shuuen")