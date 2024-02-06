SetWorkingDir %A_ScriptDir%

increment(str)
{
    Run, pythonw increment.pyw %str%
    return
}

:B0:sonic::
    increment("Sonic")

:B0:shuuen::
    increment("Shuuen")

!1::
    increment("Sonic")

!2::
    increment("Shuuen")