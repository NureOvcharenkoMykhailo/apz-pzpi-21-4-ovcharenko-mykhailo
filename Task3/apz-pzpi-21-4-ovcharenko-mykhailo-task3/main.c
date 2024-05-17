#include <curl/curl.h>
#include <json-c/json.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#define CONFIG_FILE "config.json"

typedef struct {
  char protocol[5];
  char ip[256];
  int port;
  char user_id[16];
  char locale[4];
} Config;

void read_config(Config *config) {
  FILE *file = fopen(CONFIG_FILE, "r");
  if (!file) {
    fprintf(stderr, "Could not open config file.\n");
    exit(1);
  }

  struct json_object *parsed_json;
  struct json_object *ip;
  struct json_object *port;
  struct json_object *user_id;
  struct json_object *protocol;
  struct json_object *locale;

  char buffer[1024];
  fread(buffer, 1024, 1, file);
  fclose(file);

  parsed_json = json_tokener_parse(buffer);
  json_object_object_get_ex(parsed_json, "ip", &ip);
  json_object_object_get_ex(parsed_json, "port", &port);
  json_object_object_get_ex(parsed_json, "user_id", &user_id);
  json_object_object_get_ex(parsed_json, "protocol", &protocol);
  json_object_object_get_ex(parsed_json, "locale", &locale);

  strcpy(config->ip, json_object_get_string(ip));
  config->port = json_object_get_int(port);
  strcpy(config->user_id, json_object_get_string(user_id));
  strcpy(config->protocol, json_object_get_string(protocol));
  strcpy(config->locale, json_object_get_string(locale));

  json_object_put(parsed_json);
}

// FIXME: Цю функцію потрібно прибрати коли сенсори будуть підключені.
int get_random_value(int from, int to) { return rand() % (to - from) + from; }

// Ця функція зараз генерує рандомні значення, у майбутньому вони будуть
// отримані із сенсорів.
void read_sensor_values(char *data, char *user_id) {
  int blood_pressure = get_random_value(80, 120);
  int heart_rate = get_random_value(60, 100);
  int oxygen_level = get_random_value(90, 100);

  sprintf(data,
          "{\"user_id\": \"%s\", \"blood_pressure\": %d, \"heart_rate\": %d, "
          "\"oxygen_level\": %d}",
          user_id, blood_pressure, heart_rate, oxygen_level);
}

size_t post_callback(void *ptr, size_t size, size_t nmemb, void *userdata) {
  size_t realsize = size * nmemb;
  FILE *out = fopen("received_data.json", "w");
  if (out) {
    fwrite(ptr, size, nmemb, out);
    fclose(out);
  }
  return realsize;
}

void send_post_request(const Config *config, const char *data) {
  CURL *curl;
  CURLcode res;

  curl_global_init(CURL_GLOBAL_DEFAULT);
  curl = curl_easy_init();
  if (curl) {
    char url[512];
    struct curl_httppost post;
    snprintf(url, sizeof(url), "%s://%s:%d/api/%s/iot/update", config->protocol,
             config->ip, config->port, config->locale);

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER,
                     curl_slist_append(NULL, "Content-Type: application/json"));
    curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "POST");
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);

    res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
      fprintf(stderr, "curl_easy_perform() failed: %s\n",
              curl_easy_strerror(res));
    }

    curl_easy_cleanup(curl);
  }

  curl_global_cleanup();
}

void send_get_request(const Config *config) {
  CURL *curl;
  CURLcode res;

  curl_global_init(CURL_GLOBAL_DEFAULT);
  curl = curl_easy_init();
  if (curl) {
    char url[512];
    snprintf(url, sizeof(url), "%s://%s:%d/api/%s/account/query/@%s",
             config->protocol, config->ip, config->port, config->locale,
             config->user_id);

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, post_callback);

    res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
      fprintf(stderr, "curl_easy_perform() failed: %s\n",
              curl_easy_strerror(res));
    }

    curl_easy_cleanup(curl);
  }
  curl_global_cleanup();
}

int main() {
  Config config;
  read_config(&config);

  srand(time(NULL));

  while (1) {
    char sensor_data[256];
    read_sensor_values(sensor_data, config.user_id);

    send_post_request(&config, sensor_data);

    send_get_request(&config);

    FILE *file = fopen("received_data.json", "r");
    if (file) {
      char buffer[1024];
      fread(buffer, sizeof(buffer), 1, file);
      fclose(file);
      printf("\n\nReceived Data: %s\n", buffer);
    } else {
      fprintf(stderr, "Could not open received data file.\n");
    }

    sleep(1);
  }

  return 0;
}
