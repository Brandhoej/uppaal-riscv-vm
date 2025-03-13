#define BOOL_TRUE 0xAA
#define BOOL_FALSE 0x55

#define INITIAL_VALUE 0x2a
#define PIN_SIZE 4

typedef signed char   SBYTE;
typedef unsigned char UBYTE;
typedef unsigned char BOOL;
typedef unsigned long ULONG;

UBYTE g_countermeasure;

SBYTE g_ptc = 3;
BOOL g_authenticated;
UBYTE g_userPin[PIN_SIZE] = {1, 2, 3, 4};
UBYTE g_cardPin[PIN_SIZE] = {1, 2, 3, 4};

__attribute__((always_inline)) inline void countermeasure() {
    g_countermeasure = 1;
}

BOOL verifyPIN() {
    int i;
    BOOL status;
    BOOL diff;
    g_authenticated = BOOL_FALSE;

    if(g_ptc > 0) {
        g_ptc--;

        status = BOOL_FALSE;
        diff = BOOL_FALSE;
        for(i = 0; i < PIN_SIZE; i++) {
            if(g_userPin[i] != g_cardPin[i]) {
                diff = BOOL_TRUE;
            }
        }
        if(i != PIN_SIZE) {
            countermeasure();
        }
        if (diff == BOOL_FALSE) {
            if(BOOL_FALSE == diff) {
                status = BOOL_TRUE;
            } else {
                countermeasure();
            }
        } else {
            status = BOOL_FALSE;
        }

        if(status == BOOL_TRUE) {
            if(BOOL_TRUE == status) {
                g_ptc = 3;
                g_authenticated = BOOL_TRUE; // Authentication();
                return BOOL_TRUE;
            } else {
                countermeasure();
            }
        }
    }

    return BOOL_FALSE;
}
