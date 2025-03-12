#define BOOL_TRUE 0xAA
#define BOOL_FALSE 0x55

#define INITIAL_VALUE 0x2a
#define PIN_SIZE 4

typedef signed char   SBYTE;
typedef unsigned char UBYTE;
typedef unsigned char BOOL;
typedef unsigned long ULONG;

UBYTE g_countermeasure;

SBYTE g_ptc;
BOOL g_authenticated;
UBYTE g_userPin[PIN_SIZE];
UBYTE g_cardPin[PIN_SIZE];

__attribute__((always_inline)) inline void countermeasure() {
    g_countermeasure = 1;
}

BOOL verifyPIN() {
    int i;
    BOOL status;
    BOOL diff;
    int stepCounter;
    SBYTE ptcCpy = g_ptc;
    g_authenticated = BOOL_FALSE;

    if(g_ptc > 0) {
        if(ptcCpy != g_ptc) {
            countermeasure();
        }
        g_ptc--;
        if(g_ptc != ptcCpy-1) {
            countermeasure();
        }
        ptcCpy--;

        status = BOOL_FALSE;
        diff = BOOL_FALSE;
        stepCounter = 0;
        for(i = 0; i < PIN_SIZE; i++) {
            if(g_userPin[i] != g_cardPin[i]) {
                diff = BOOL_TRUE;
            }
            stepCounter++;
        }
        if(stepCounter != PIN_SIZE) {
            countermeasure();
        }
        if(i != PIN_SIZE) {
            countermeasure();
        }
        if (diff == BOOL_FALSE) {
            status = BOOL_TRUE;
        } else {
            status = BOOL_FALSE;
        }

        if(status == BOOL_TRUE) {
            if(ptcCpy != g_ptc) {
                countermeasure();
            }
            g_ptc = 3;
            g_authenticated = BOOL_TRUE; // Authentication();
            return BOOL_TRUE;
        }
    }

    return BOOL_FALSE;
}
