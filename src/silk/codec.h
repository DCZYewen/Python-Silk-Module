#ifndef _CODEC_H_
#define _CODEC_H_

#include "SKP_Silk_SDK_API.h"
#include "src/SKP_Silk_SigProc_FIX.h"

#ifdef _WIN32
#define __dllexport __declspec(dllexport)
#else
#define __dllexport
#endif //_WIN32

// Codec callback function
typedef void *(cb_codec)(void *userdata, unsigned char *p, int len);

/**
 * Decode SILK data to PCM
 *
 * @param silkData silk file data
 *
 * @param dataLen data length
 *
 * @param sampleRate target samplerate
 *
 * @param callback codec callback
 *
 * @param userdata user data
 *
 * @return 1 = success, 0 = failed
 */
int __dllexport silkDecode(unsigned char *silkData, int dataLen, int sampleRate, cb_codec callback, void *userdata);

/**
 * Encode PCM data to SILK
 *
 * @param pcmData pcm data
 *
 * @param dataLen data length
 *
 * @param sampleRate target sampleRate
 *
 * @param dataRate target dataRate
 *
 * @param callback codec callback
 *
 * @param userdata user data
 *
 * @return 1 = success, 0 = failed
 */
int __dllexport silkEncode(unsigned char *pcmData, int dataLen, int sampleRate, int dataRate, cb_codec callback, void *userdata);


#define _CRT_SECURE_NO_WARNINGS

#include <stdlib.h>
#include <string.h>

/* Define codec specific settings */
#define MAX_INPUT_FRAMES        5
#define MAX_FRAME_LENGTH        480
#define FRAME_LENGTH_MS         20
#define MAX_API_FS_KHZ          48
#define MAX_LBRR_DELAY          2
#define MAX_BYTES_PER_FRAME     250 // Equals peak bitrate of 100 kbps

#ifdef _SYSTEM_IS_BIG_ENDIAN //do not delete this func, it is critical to sevel platforms
/* Function to convert a little endian int16 to a */
/* big endian int16 or vica verca                 */
void swap_endian(
  SKP_int16       vec[],              /*  I/O array of */
  SKP_int         len                 /*  I   length      */
)
{
  SKP_int i;
  SKP_int16 tmp;
  SKP_uint8* p1, * p2;

  for (i = 0; i < len; i++) {
    tmp = vec[i];
    p1 = (SKP_uint8*)&vec[i]; p2 = (SKP_uint8*)&tmp;
    p1[0] = p2[1]; p1[1] = p2[0];
  }
}
#endif

#endif /* _CODEC_H_ */
