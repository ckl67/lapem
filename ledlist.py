# -------------
# Led Nothing
# -------------
# Mode : "Static", "Blinck", "Infinity"
# For Static we will take the "ONT" status
# For Dynamic we will end by OFFT
LedPlayNothing = { 
        "Mode"   : "Static", 
        "ONT"    : 0,
        "OFFT"   : 0,
        "NbL"    : 1
        }

LedPowerNothing = {
        "Mode"   : "Static", 
        "ONT"    : 1,
        "OFFT"   : 0,
        "NbL"    : 1
        }

LedNothing = [LedPlayNothing, LedPowerNothing]

# -------------
# Led Play
# -------------
# Mode : "Static", "Blinck", "Infinity"
# For Static we will take the "ONT" status
# For Dynamic we will end by OFFT
LedPlayPlay = { 
        "Mode"   : "Static", 
        "ONT"    : 1,
        "OFFT"   : 0,
        "NbL"    : 1
        }

LedPowerPlay = {
        "Mode"   : "Static", 
        "ONT"    : 1,
        "OFFT"   : 0,
        "NbL"    : 1
        }

LedPlay = [LedPlayPlay, LedPowerPlay]

# -------------
# Led Pause
# -------------
# Mode : "Static", "Blinck", "Infinity"
# For Static we will take the "ONT" status
# For Dynamic we will end by OFFT
LedPlayPause = { 
        "Mode"   : "Static", 
        "ONT"    : 0,
        "OFFT"   : 0,
        "NbL"    : 5
        }

LedPowerPause = {
        "Mode"   : "Static", 
        "ONT"    : 1,
        "OFFT"   : 0,
        "NbL"    : 1
        }

LedPause = [LedPlayPause, LedPowerPause]

# -------------
# Led Back
# -------------
# Mode : "Static", "Blinck", "Infinity"
# For Static we will take the "ONT" status
# For Dynamic we will end by OFFT
LedPlayBack = { 
        "Mode"   : "Blink", 
        "ONT"    : 0.5,
        "OFFT"   : 0.5,
        "NbL"    : 3
        }

LedPowerBack = {
        "Mode"   : "Static", 
        "ONT"    : 1,
        "OFFT"   : 0,
        "NbL"    : 1
        }

LedBack = [LedPlayBack, LedPowerBack]

# -------------
# -------------

LapemMode = { 
        'Nothing'   : LedNothing,
        'Play'      : LedPlay,
        'Pause'     : LedPause,
        'Back'      : LedBack, 
        }

ID_LED_PLAY = 0
ID_LED_POWER = 1

cState = "Nothing"

print(LapemMode[cState][ID_LED_POWER]["Mode"])



