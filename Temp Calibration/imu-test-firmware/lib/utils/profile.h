#include "DebugLog.h"

#define PROFILE_FUNCTION(func) \
    do { \
        unsigned long startTime = millis(); \
        func; \
        unsigned long duration = millis() - startTime; \
        LOG_DEBUG(F(#func " duration: "), duration); \
    } while (0)