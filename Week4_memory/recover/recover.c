#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    if(argc!=2){
        printf("Usage: ./recover card.raw\n");
        return 1;
    }
    FILE *file = fopen(argv[1],"r");
    if(file==NULL){
        printf("Cannot open the file\n");
        return 1;
    }
    int image_count=0;
    char filename[8];
    uint8_t buffer[512];
    FILE *new_file = NULL;
    while(fread(buffer, 1, 512, file) == 512){
        if(buffer[0]==0xff && buffer[1]==0xd8 && buffer[2]==0xff && (buffer[3] & 0xf0) == 0xe0){
            if(new_file!=NULL) fclose(new_file);
            sprintf(filename, "%03i.jpg", image_count);
            new_file = fopen(filename, "w");
            if(new_file==NULL) {
                printf("Cannot open new file for image\n");
                fclose(file);
                return 1;
            }
            ++image_count;
        }
        if(new_file != NULL){
            fwrite(buffer, sizeof(uint8_t), 512, new_file);
        }
    }
    if(new_file!=NULL) fclose(new_file);
    fclose(file);
    return 0;
}
