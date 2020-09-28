import pyo

# Interpolations utility

def lerp(x, x_a, x_b, y_a, y_b):
    return (y_a + (y_b - y_a) * ((x - x_a)/(x_b - x_a)))

def nlerp(x, y_a, y_b):
    return (lerp(x, 0, 1, y_a, y_b))

# Wrapper functions around ugens

## SYNTHS

def blit(f=0.5, harms=0.5):
    return pyo.Blit(freq=nlerp(f, 27, 6912),
                    harms=nlerp(harms, 0, 100))

def crossfm(f=0.5, ratio=0.5, ind1=0.5, ind2=0.5):
    return pyo.CrossFM(carrier=nlerp(f, 27, 6912),
                       ratio=ratio,
                       ind1=nlerp(ind1, 0, 2),
                       ind2=nlerp(ind2, 0, 2))

def fsine(f=0.5):
    return pyo.FastSine(freq=nlerp(f, 27, 6912),
                        initphase=0,
                        quality=1)

def phasor(f=0.5, phase=0.5):
    return pyo.Phasor(freq=nlerp(f, 27, 6912),
                      phase=phase)

def rcosc(f=0.5, sharp=0.5):
    return pyo.RCOsc(freq=nlerp(f, 27, 6912),
                     sharp=sharp)

def sineloop(f=0.5, feedback=0.5):
    return pyo.SineLoop(freq=nlerp(f, 27, 6912),
                        feedback=feedback)

def supersaw(f=0.5, detune=0.5, bal=0.5):
    return pyo.SuperSaw(freq=nlerp(f, 27, 6912),
                        detune=detune,
                        bal=bal)

## LFOS

def sawuplfo(f=0.5, sharp=0.5):
    return pyo.LFO(freq=nlerp(f, 0.1, 10),
                   sharp=sharp,
                   type=0)

def sawdownlfo(f=0.5, sharp=0.5):
    return pyo.LFO(freq=nlerp(f, 0.1, 10),
                   sharp=sharp,
                   type=1)

def squarelfo(f=0.5, sharp=0.5):
    return pyo.LFO(freq=nlerp(f, 0.1, 10),
                   sharp=sharp,
                   type=2)

def trilfo(f=0.5, sharp=0.5):
    return pyo.LFO(freq=nlerp(f, 0.1, 10),
                   sharp=sharp,
                   type=3)

def pulselfo(f=0.5, sharp=0.5):
    return pyo.LFO(freq=nlerp(f, 0.1, 10),
                   sharp=sharp,
                   type=4)

def bipulselfo(f=0.5, sharp=0.5):
    return pyo.LFO(freq=nlerp(f, 0.1, 10),
                   sharp=sharp,
                   type=5)

def shlfo(f=0.5, sharp=0.5):
    return pyo.LFO(freq=nlerp(f, 0.1, 10),
                   sharp=sharp,
                   type=6)

def modsinelfo(f=0.5, sharp=0.5):
    return pyo.LFO(freq=nlerp(f, 0.1, 10),
                   sharp=sharp,
                   type=7)

## FX

def disto(input=0, drive=0.5, slope=0.5):
    if isinstance(input, float):
        input = pyo.Sig(input)
    return pyo.Disto(input=input,
                     drive=drive,
                     slope=slope)

def delay(input=0, delay=0.5, feedback=0):
    if isinstance(input, float):
        input = pyo.Sig(input)
    return pyo.Delay(input=input,
                     delay=nlerp(delay, 0, 4),
                     feedback=feedback,
                     maxdelay=4)

def freeverb(input=0, size=0.5, damp=0.5, bal=0.5):
    if isinstance(input, float):
        input = pyo.Sig(input)
    return pyo.Freeverb(input=input,
                        size=size,
                        damp=damp,
                        bal=bal)

def chorus(input=0, depth=0.5, feedback=0.5, bal=0.5):
    if isinstance(input, float):
        input = pyo.Sig(input)
    return pyo.Chorus(input=input,
                      depth=nlerp(depth, 0, 5),
                      feedback=feedback,
                      bal=bal)

## ARITHMETICS

def tanh(input=0):
    if isinstance(input, float):
        input = pyo.Sig(input)
    return pyo.Tanh(input)