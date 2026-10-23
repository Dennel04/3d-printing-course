// XIAO ESP32S3 Sense tool camera.
// The lab PC has no WiFi, so frames go over the USB serial port:
//   host sends 'c'  -> board answers "JPG <bytes>\n" followed by the JPEG
//   host sends 'i'  -> board answers one status line
// Pin map: CAMERA_MODEL_XIAO_ESP32S3 from the Arduino CameraWebServer example.
#include <Arduino.h>
#include "esp_camera.h"

static bool camera_ok = false;

static bool camera_init() {
  camera_config_t c = {};
  c.pin_pwdn = -1;
  c.pin_reset = -1;
  c.pin_xclk = 10;
  c.pin_sccb_sda = 40;
  c.pin_sccb_scl = 39;
  c.pin_d7 = 48;
  c.pin_d6 = 11;
  c.pin_d5 = 12;
  c.pin_d4 = 14;
  c.pin_d3 = 16;
  c.pin_d2 = 18;
  c.pin_d1 = 17;
  c.pin_d0 = 15;
  c.pin_vsync = 38;
  c.pin_href = 47;
  c.pin_pclk = 13;
  c.xclk_freq_hz = 20000000;
  c.ledc_timer = LEDC_TIMER_0;
  c.ledc_channel = LEDC_CHANNEL_0;
  c.pixel_format = PIXFORMAT_JPEG;
  c.frame_size = FRAMESIZE_UXGA;  // 1600x1200, needs PSRAM
  c.jpeg_quality = 10;
  c.fb_count = 2;
  c.fb_location = CAMERA_FB_IN_PSRAM;
  c.grab_mode = CAMERA_GRAB_LATEST;
  esp_err_t err = esp_camera_init(&c);
  if (err != ESP_OK) {
    Serial.printf("ERR camera init 0x%x\n", err);
    return false;
  }
  return true;
}

static void send_frame() {
  if (!camera_ok) {
    Serial.println("ERR camera not ready");
    return;
  }
  // Drop stale frames so exposure matches the scene right now.
  for (int i = 0; i < 2; i++) {
    camera_fb_t *old = esp_camera_fb_get();
    if (old) esp_camera_fb_return(old);
  }
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("ERR capture failed");
    return;
  }
  Serial.printf("JPG %u\n", (unsigned)fb->len);
  Serial.write(fb->buf, fb->len);
  Serial.flush();
  esp_camera_fb_return(fb);
}

void setup() {
  Serial.begin(115200);
  camera_ok = camera_init();
  if (camera_ok) {
    sensor_t *s = esp_camera_sensor_get();
    Serial.printf("READY sensor PID 0x%x\n", s->id.PID);
  }
}

void loop() {
  if (!Serial.available()) {
    delay(5);
    return;
  }
  char cmd = Serial.read();
  if (cmd == 'c') {
    send_frame();
  } else if (cmd == 'i') {
    sensor_t *s = camera_ok ? esp_camera_sensor_get() : nullptr;
    Serial.printf("INFO camera=%s pid=0x%x psram=%u\n", camera_ok ? "ok" : "fail",
                  s ? s->id.PID : 0, (unsigned)ESP.getPsramSize());
  }
}
