#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
} pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

int findCandidate(string name){
    for(int i=0;i<candidate_count;++i){
        if(strcmp(candidates[i],name)==0){
            return i;
        }
    }
    return -1;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // TODO
    if(findCandidate(name)<0)return false;
    ranks[rank] = findCandidate(name);
    return true;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // TODO
    for(int i=0;i<candidate_count;++i){
        for(int j=i+1;j<candidate_count;++j){
            preferences[ranks[i]][ranks[j]]++;
        }
    }
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // TODO
    for(int i=0;i<candidate_count;++i){
        for(int j=i+1;j<candidate_count;++j){
            if(i!=j){
                if(preferences[i][j]>preferences[j][i]){
                    pairs[pair_count].winner = i;
                    pairs[pair_count].loser = j;
                    ++pair_count;
                }
                if(preferences[i][j]<preferences[j][i]){
                    pairs[pair_count].winner = j;
                    pairs[pair_count].loser = i;
                    ++pair_count;
                }
            }
        }
    }
}

int compare(const void* a, const void* b){
    pair* pairA = (pair*)a;
    pair* pairB = (pair*)b;
    int strengthA = preferences[pairA->winner][pairA->loser];
    int strengthB = preferences[pairB->winner][pairB->loser];
    return strengthB - strengthA;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // TODO
    qsort(pairs,pair_count,sizeof(pair),compare);

}

bool DFS_check_cycle(int w, int l){
    if(w==l)return true;
    for(int i=0;i<candidate_count;++i){
        if(locked[l][i]){
            if(DFS_check_cycle(w,i)){
                return true;
            }
        }
    }
    return false;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // TODO
    for (int i=0;i<pair_count; i++){
        if (!DFS_check_cycle(pairs[i].winner,pairs[i].loser)){
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
}

// Print the winner of the election
void print_winner(void)
{
    // TODO
    for(int i=0;i<candidate_count;++i){
        bool all_false = true;
        for(int j=0; j<candidate_count;++j){
            if(i==j)continue;
            if(locked[j][i]==true){
                all_false = false;
            }
        }
        if(all_false==true){
            printf("%s\n", candidates[i]);
            return;
        }
    }
}


