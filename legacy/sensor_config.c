#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <limits.h>

static int invalid(const char *field) {
    printf("{\"ok\":false,\"error\":{\"code\":\"INVALID_REQUEST\",\"field\":\"%s\"}}\n", field);
    return 0;
}
int main(int argc, char **argv) {
    const char *fields[] = {"sampleMs", "gain", "offsetMilli", "rawMilli", "alarmLowMilli", "alarmHighMilli", "enabled"};
    const long lo[] = {10,1,-100000,-1000000,-20000000,-20000000,0};
    const long hi[] = {60000,16,100000,1000000,20000000,20000000,1};
    long v[7];
    if (argc != 9) return invalid("$");
    int temperature = strcmp(argv[1], "temperature") == 0;
    if (!temperature && strcmp(argv[1], "pressure") != 0) return invalid("profile");
    for (int i=0; i<7; i++) {
        char *end; errno=0; v[i]=strtol(argv[i+2], &end, 10);
        if (errno || *end || end==argv[i+2] || v[i]<lo[i] || v[i]>hi[i]) return invalid(fields[i]);
    }
    if (v[4]>=v[5]) return invalid("alarmHighMilli");
    long sample=((v[0]+9)/10)*10;
    long reading=v[3]*v[1]+v[2];
    long minimum=temperature?-40000:0, maximum=temperature?125000:1000000;
    int clamped=reading<minimum || reading>maximum;
    if (reading<minimum) reading=minimum;
    if (reading>maximum) reading=maximum;
    const char *state=!v[6]?"disabled":reading<v[4]?"low":reading>v[5]?"high":"ok";
    printf("{\"ok\":true,\"profile\":\"%s\",\"effectiveSampleMs\":%ld,\"readingMilli\":%ld,\"status\":\"%s\",\"warnings\":[",argv[1],sample,reading,state);
    if (sample!=v[0]) printf("\"sample-rounded\"");
    if (clamped) printf("%s\"reading-clamped\"",sample!=v[0]?",":"");
    puts("]}");
    return 0;
}
