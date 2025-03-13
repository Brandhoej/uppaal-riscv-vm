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

__attribute__((always_inline)) inline BOOL byteArrayCompare(UBYTE* a1, UBYTE* a2, UBYTE size) {
    int i;
    BOOL status = BOOL_FALSE;
    BOOL diff = BOOL_FALSE;
    for(i = 0; i < size; i++) {
        if(a1[i] != a2[i]) {
            diff = BOOL_TRUE;
        }
    }
    if(i != size) {
        countermeasure();
    }
    if (diff == BOOL_FALSE) {
        status = BOOL_TRUE;
    } else {
        status = BOOL_FALSE;
    }
    return status;
}

BOOL verifyPIN() {
    g_authenticated = BOOL_FALSE;

    if(g_ptc > 0) {
        g_ptc--;

        if(byteArrayCompare(g_userPin, g_cardPin, PIN_SIZE) == BOOL_TRUE) {
            if(byteArrayCompare(g_cardPin, g_userPin, PIN_SIZE) == BOOL_TRUE) {
                g_ptc = 3;
                g_authenticated = BOOL_TRUE; // Authentication();
                return BOOL_TRUE;
            } else countermeasure();
        }
    }

    return BOOL_FALSE;
}
