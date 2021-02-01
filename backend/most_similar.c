#include <stdlib.h>
#include <stdio.h>
#include <time.h>

static int matrix[1000000][128];
//static float dis_vect[500000];

struct distanceID {
    int id;
    int dis;
};

int compare( const void* a, const void* b){
        return -( (*(struct distanceID*)b).dis - (*(struct distanceID*)a).dis );
    }

int* most_similar(int y, int row, int matrix[row][128], int target[128], int* result )
{  
    
    int dis_vect[row*2];
 
    #pragma omp parallel for
    for(int j = 0; j<row*2; j+=2){
        int dis = 0;
        for(int l = 0; l<256; l+=2){
            int tar = target[l]-matrix[j][l];
            dis += tar*tar;
        }
        dis_vect[j] = dis;
    }
    struct distanceID distances[row];
    for(int x = 0; x<row; x++){
        distances[x].id = x;
        distances[x].dis = dis_vect[x*2];
    }

    //printf("%f\n",distances[0].dis);
    //printf("%f\n",distances[1].dis);
    //printf("%f\n",distances[2].dis);
    qsort( distances, row, sizeof(struct distanceID), compare );

    for(int z = 0; z<y; z++){
        result[z] = distances[z].id;
    }
    
        return result;
}

int main(){


int target[128];
    int i, o, k, j, l;
int result[10];
for(o = 0; o<500000; o++)
        for(i = 0; i<128; i++)
            matrix[o][i] = rand()%100;

    for(k = 0; k<128; k++){
        target[k] = rand()%100;
    }

int* a = most_similar(10,500000,matrix,target,result);
for(int y=0; y<10;y++){
	printf("%d\n",a[y]);
}
    	return 0;

}
