struct person{
    uint8_t id[7];      // UID for the NFC tag for the guest
    uint8_t branch;     // which LED string the guest is on
    uint16_t* path;     // an array with LED indices that define the 
                        // path of LEDs to the guest's seat on the map
    uint8_t pathLen;    // number of LEDs in the path to guests's seat
};

#define NUM_GUESTS 5
struct person guests[] = {
    {
    .id = {0x04, 0xC2, 0x64, 0x25, 0x6F, 0x61, 0x80},
    .branch = 0
    },
    {
    .id = {0x04, 0x83, 0x58, 0x69, 0x8F, 0x61, 0x80},
    .branch = 1
    },
    {
    .id = {0x04, 0xF3, 0x63, 0x35, 0x5F, 0x61, 0x80},
    .branch = 1
    },
    {
    .id = {0x04, 0x44, 0x48, 0x20, 0x6F, 0x61, 0x80},
    .branch = 0
    },
    {
    .id = {0x04, 0x9E, 0x18, 0x54, 0x6F, 0x61, 0x80},
    .branch = 0
    }
};

uint8_t pathLen0 = 11;
uint16_t path0[] = {75,74,73,72,71,70,69,68,67,55,52};
uint8_t pathLen1 = 13;
uint16_t path1[] = {75,74,73,72,71,70,69,68,67,54,54,52,51};
uint8_t pathLen2 = 18;
uint16_t path2[] = {75,74,73,72,71,70,69,68,67,66,55,54,31,32,33,34,35,36};
uint8_t pathLen3 = 12;
uint16_t path3[] = { 9,10,11,12,13,14,15,16,17,18,19,20};
uint8_t pathLen4 = 11;
uint16_t path4[] = { 9,10,11,12,13,14,15,16,17,18,19};