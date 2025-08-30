#ifndef SHARED_H
#define SHARED_H

#include "mumble/Mumble.h"
#include "nexus/Nexus.h"
#include "rtapi/RTAPI.hpp"

extern AddonAPI_t *APIDefs;
extern Mumble::Data *MumbleLink;
extern Mumble::Identity *MumbleIdentity;
extern NexusLinkData_t *NexusLink;
extern RTAPI::RealTimeData *RTAPIData;

#endif
