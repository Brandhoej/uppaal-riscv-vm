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
UBYTE g_cardPin[PIN_SIZE] = {1, 2, 3, 4};

__attribute__((always_inline)) inline void countermeasure() {
    g_countermeasure = 1;
}

__attribute__((always_inline)) inline BOOL byteArrayCompare(UBYTE* a1, UBYTE* a2, UBYTE size) {
    int i;
    for(i = 0; i < size; i++) {
        if(a1[i] != a2[i]) {
            return BOOL_FALSE;
        }
    }
    return BOOL_TRUE;
}

BOOL verifyPIN() {
    int comp;
    g_authenticated = BOOL_FALSE;

    if(g_ptc > 0) {
        comp = byteArrayCompare(g_userPin, g_cardPin, PIN_SIZE);
        if(comp == BOOL_TRUE) {
            g_ptc = 3;
            g_authenticated = BOOL_TRUE; // Authentication();
            return BOOL_TRUE;
        } else if(comp == BOOL_FALSE) {
          g_ptc--;
          return BOOL_FALSE;
        } else {
          countermeasure();
        }
    }
    return BOOL_FALSE;
}