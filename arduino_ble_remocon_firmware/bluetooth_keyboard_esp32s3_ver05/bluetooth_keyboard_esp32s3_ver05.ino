/**
 * This example turns the ESP32 into a Bluetooth LE keyboard that writes the words, presses Enter, presses a media key and then Ctrl+Alt+Delete
 */
#include "BleKeyboard.h"
#include <Preferences.h>
#include "DeviceName.h"  /** First, Activate "get_device_name.py", after this file*/

static const String CMD_START = "s";
static const String CMD_STOP = "S";
static const String CMD_WRITE_KEY_CODE = "w";
static const String CMD_WRITE_MEDIA_KEY_CODE = "W";
static const String CMD_PRESS_KEY_CODE = "p";
static const String CMD_PRESS_MEDIA_KEY_CODE = "P";
static const String CMD_RELEASE_KEY_CODE = "t";
static const String CMD_RELEASE_MEDIA_KEY_CODE = "T";
static const String CMD_RELEASE_ALL = "x";

static const String CMD_WRITE_STRING = "o";

static const String CMD_SET_DELAY = "d";
static const String CMD_SET_DEVICE_NAME = "n";
static const String CMD_GET_DEVICE_NAME = "N";
static const String CMD_GET_DEVICE_TYPE = "y";
static const String CMD_GET_DEVICE_STATUS = "g";

static const String CMD_LONG_PRESS = "l";
static const String CMD_REPEAT = "r";
static const String CMD_DISCONNECT = "D";

String cmd_str = "";
String cmd_tokens[20];
int command_token_count = 0;
String board_id = String(DEVICE_NAME);
BleKeyboard bleKeyboard;

Preferences preferences;



void split_cmd_str(String cmd_str)
{
  command_token_count = 0;
  for (int i = 0; i < 20; i++)
  {
    cmd_tokens[i] = "";
  }
  // Split the string into substrings
  while (cmd_str.length() > 0 && command_token_count < 20)
  {
    int index = cmd_str.indexOf(' ');
    if (index == -1) // No space found
    {
      cmd_tokens[command_token_count++] = cmd_str;
      break;
    }
    else
    {
      cmd_tokens[command_token_count++] = cmd_str.substring(0, index);
      cmd_str = cmd_str.substring(index + 1);
    }
  }
}

void print_cmd_tokens()
{
  Serial.println("---------------");
  for (int i = 0; i < 20; i++)
  {
    if (cmd_tokens[i].length() > 0)
    {
      Serial.println(cmd_tokens[i]);
    }
  }
  Serial.println("---------------");
}

/* create a hardware timer */
hw_timer_t *timer = NULL;

/* LED pin */
int led = 1;
/* LED state */
volatile byte state = LOW;

void IRAM_ATTR onTimer()
{
  state = !state;
  digitalWrite(led, state);
}

void setup()
{
  Serial.begin(115200);
  Serial.println("Starting BLE work!");
  Serial.flush();
  Serial.print("Device name: ");
  Serial.println(board_id);

  // Bluetooth key event output init
  pinMode(12, OUTPUT);
  digitalWrite(12, LOW);

  // get env data from eeprom
  preferences.begin("board_info", false);
  board_id = preferences.getString("board_id", board_id);
  //[E][Preferences.cpp:483] getString(): nvs_get_str len fail: board_id NOT_FOUND
  preferences.end();
  // ble init
  bleKeyboard = BleKeyboard(std::string(board_id.c_str()), "NextLab", 100);

  // led  blinking init
  pinMode(led, OUTPUT);
  digitalWrite(led, state);
  /* Use 1st timer of 4 */
  /* 1 tick take 1/(80MHZ/80) = 1us so we set divider 80 and count up */
  timer = timerBegin(2, 80, true);
  /* Attach onTimer function to our timer */
  timerAttachInterrupt(timer, &onTimer, false); // true가 안된다.
  // W][esp32-hal-timer.c:226] timerAttachInterruptFlag(): EDGE timer interrupt is not supported! Setting to LEVEL...
  /* Set alarm to call onTimer function every second 1 tick is 1us
  => 1 second is 1000000us */
  /* Repeat the alarm (third parameter) */
  timerAlarmWrite(timer, 500000, true);
  /* Start an alarm */
  timerAlarmEnable(timer);
}

// we need mappings here

void loop()
{
  if (bleKeyboard.isConnected())
  {
    cmd_str = Serial.readStringUntil('\n');
    if (cmd_str.length() > 0)
    {
      Serial.println(cmd_str); // 이거 계속 할 것인가?
      split_cmd_str(cmd_str);
      if (cmd_tokens[0] == CMD_GET_DEVICE_NAME)
      {
        preferences.begin("board_info", false);
        board_id = preferences.getString("board_id", board_id);
        preferences.end();
        Serial.println(board_id);
      }
      else if (cmd_tokens[0] == CMD_GET_DEVICE_TYPE)
      {
        Serial.println("DEVICE_TYPE:BLUETOOTH");
      }
      else if (cmd_tokens[0] == CMD_GET_DEVICE_STATUS)
      {
        Serial.println("status:connected");
      }

      else if (cmd_tokens[0] == CMD_WRITE_KEY_CODE)
      {
        uint8_t key_code = cmd_tokens[1].toInt();
        digitalWrite(12, HIGH);
        bleKeyboard.write((uint8_t)key_code);
        digitalWrite(12, LOW);
        Serial.println("write done");
      }
      else if (cmd_tokens[0] == CMD_WRITE_MEDIA_KEY_CODE)
      {
        int number = (int)strtol(cmd_tokens[1].c_str(), NULL, 16);
        uint8_t media_key_high = (uint8_t)((number & 0xFF00) >> 8);
        uint8_t media_key_low = (uint8_t)(number & 0x00FF);
        // FF를 max로 잡아야 하지만...
        MediaKeyReport media_key = {media_key_low, media_key_high};
        Serial.print(media_key_high);
        Serial.print(media_key_low);
        // TODO: add validity check
        //  if (key_index > 0)
        //  {
        digitalWrite(12, HIGH);
        bleKeyboard.write(media_key);
        digitalWrite(12, LOW);
        Serial.println("write done");
        // }
        // else
        // {
        //   Serial.println("write fail: invalid index");
        // }
      }
      else if (cmd_tokens[0] == CMD_PRESS_KEY_CODE)
      {
        uint8_t key_code = cmd_tokens[1].toInt();
        digitalWrite(12, HIGH);
        bleKeyboard.press((uint8_t)key_code);
        digitalWrite(12, LOW);
        Serial.println("press done");

      }
      else if (cmd_tokens[0] == CMD_PRESS_MEDIA_KEY_CODE)
      {
        int number = (int)strtol(cmd_tokens[1].c_str(), NULL, 16);
        uint8_t media_key_high = (uint8_t)((number & 0xFF00) >> 8);
        uint8_t media_key_low = (uint8_t)(number & 0x00FF);

        MediaKeyReport media_key = {media_key_low, media_key_high};
        // TODO: add validity check
        //  if (key_index > 0)
        //  {
        digitalWrite(12, HIGH);
        bleKeyboard.press(media_key);
        digitalWrite(12, LOW);
        Serial.println("press done");
        // }
        // else
        // {
        //   Serial.println("write fail: invalid index");
        // }
      }
      else if (cmd_tokens[0] == CMD_RELEASE_KEY_CODE)
      {
        uint8_t key_code = cmd_tokens[1].toInt();
        bleKeyboard.release((uint8_t)key_code);
        Serial.println("release done");
      }
      else if (cmd_tokens[0] == CMD_RELEASE_MEDIA_KEY_CODE)
      {
        int number = (int)strtol(cmd_tokens[1].c_str(), NULL, 16);
        uint8_t media_key_high = (uint8_t)((number & 0xFF00) >> 8);
        uint8_t media_key_low = (uint8_t)(number & 0x00FF);

        MediaKeyReport media_key = {media_key_low, media_key_high};
        // TODO: add validity check
        //  if (key_index > 0)
        //  {
        digitalWrite(12, HIGH);
        bleKeyboard.release(media_key);
        digitalWrite(12, LOW);
        Serial.println("release done");
        // }
        // else
        // {
        //   Serial.println("write fail: invalid index");
        // }
      }
      else if (cmd_tokens[0] == CMD_RELEASE_ALL)
      {
        bleKeyboard.releaseAll();
        Serial.println("release all done");
      }
      else if (cmd_tokens[0] == CMD_WRITE_STRING)
      {
        uint8_t key_code = 0;
        // digitalWrite(12, HIGH);
        for (int i = 1; i < command_token_count; i++)
        {
          key_code = cmd_tokens[i].toInt();
          bleKeyboard.write((uint8_t)key_code);
        }
        Serial.println("write string done");
      }
      else if (cmd_tokens[0] == CMD_LONG_PRESS)
      {
        int key_code = cmd_tokens[1].toInt();
        int duration = cmd_tokens[2].toInt();
        digitalWrite(12, HIGH);
        bleKeyboard.press((uint8_t)key_code);
        digitalWrite(12, LOW);
        delay(duration);
        bleKeyboard.release((uint8_t)key_code);
        Serial.println("press done");
      }
      else if (cmd_tokens[0] == CMD_REPEAT)
      {
        int key_code = cmd_tokens[1].toInt();
        int repeat = cmd_tokens[3].toInt();
        int interval = cmd_tokens[2].toInt();
        for (int i = 0; i < repeat; i++)
        {
          digitalWrite(12, HIGH);
          bleKeyboard.write((uint8_t)key_code);
          digitalWrite(12, LOW);
          delay(interval);
        }
        Serial.println("repeat done");
      }
      else if (cmd_tokens[0] == CMD_STOP)
      {
        Serial.println("restarting ble keyboard device");
        delay(100);
        ESP.restart();
      }
      else if (cmd_tokens[0] == CMD_DISCONNECT)
      {
        delay(100);
        bleKeyboard.disconnect();
        Serial.println("disconnecting done");
        delay(3000);
        ESP.restart();
      }
      else if (cmd_tokens[0] == CMD_SET_DELAY)
      {
        uint32_t delay_in_ms = cmd_tokens[1].toInt();
        bleKeyboard.setDelay(delay_in_ms);
        Serial.println("delay_changed");
      }
      else if (cmd_tokens[0] == CMD_SET_DEVICE_NAME || cmd_tokens[0] == CMD_START)
      {
        Serial.println("already connected.");
      }
      // print_cmd_tokens();
      cmd_str = "";
    }
  }
  else
  {
    cmd_str = Serial.readStringUntil('\n');
    if (cmd_str.length() > 0)
    {
      Serial.println(cmd_str);
      split_cmd_str(cmd_str);
      if (cmd_tokens[0] == CMD_GET_DEVICE_NAME)
      {
        preferences.begin("board_info", false);
        board_id = preferences.getString("board_id", board_id);
        preferences.end();
        Serial.println(board_id);
      }
      else if (cmd_tokens[0] == CMD_GET_DEVICE_TYPE)
      {
        Serial.println("DEVICE_TYPE:BLUETOOTH");
      }
      else if (cmd_tokens[0] == CMD_SET_DEVICE_NAME)
      {
        String board_id_in = cmd_tokens[1];
        preferences.begin("board_info", false);
        preferences.putString("board_id", board_id_in);
        board_id = board_id_in;
        Serial.println(board_id);
      }
      else if (cmd_tokens[0] == CMD_START)
      {
        Serial.print("Device name: ");
        Serial.println(board_id);
        Serial.println("connecting....");
        bleKeyboard.begin();
        Serial.println("connecting....");
        while (!bleKeyboard.isConnected())
        {
          Serial.println("waiting for connection...");
          cmd_str = Serial.readStringUntil('\n');
          if (cmd_tokens[0] == CMD_STOP)
          {
            Serial.println("restarting ble keyboard device");
            delay(100);
            ESP.restart();
          }
          else if (cmd_tokens[0] == CMD_GET_DEVICE_STATUS)
          {
            Serial.println("status:connecting");
          }
          delay(4000);
        }
        Serial.println("connected");
      }
      else if (cmd_tokens[0] == CMD_GET_DEVICE_STATUS)
      {
        Serial.println("status:stoped");
      }
      else if (cmd_tokens[0] == CMD_STOP)
      {
        Serial.println("device will stop....");
        delay(100);
        ESP.restart();
      }
      else if (cmd_tokens[0] == CMD_DISCONNECT)
      {
        Serial.println("device disconnected. It will be restarted....");
        delay(100);
        ESP.restart();
      }
      else if (
          cmd_tokens[0] == CMD_WRITE_KEY_CODE ||
          cmd_tokens[0] == CMD_WRITE_MEDIA_KEY_CODE ||
          cmd_tokens[0] == CMD_LONG_PRESS ||
          cmd_tokens[0] == CMD_REPEAT ||
          cmd_tokens[0] == CMD_PRESS_KEY_CODE ||
          cmd_tokens[0] == CMD_RELEASE_KEY_CODE ||
          cmd_tokens[0] == CMD_PRESS_MEDIA_KEY_CODE ||
          cmd_tokens[0] == CMD_RELEASE_MEDIA_KEY_CODE ||
          cmd_tokens[0] == CMD_RELEASE_ALL ||
          cmd_tokens[0] == CMD_WRITE_STRING ||
          cmd_tokens[0] == CMD_SET_DELAY)
      {
        Serial.println("device not started");
      }
      // print_cmd_tokens();
      cmd_str = "";
    }
  }

  delay(100);
}