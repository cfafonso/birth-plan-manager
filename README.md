# birth-plan-manager
This is a command-line tool in object-oriented python that manages childbirth assistances in a hospital setting. It processes three text files containing records of doctors, existing schedules, and pending assistance requests to produce two new text files containing an updated calendar of childbirth assistances and a revised list of available doctors.


## Prerequisites

- Python 3.x


## Usage

1. Place the required input files contained within the `testSets` folder inside the `birthPlan` folder. For instance, in the case of `testSet1`, these would be:
  - The `doctors10h00.txt`
  - The `schedule10h00.txt`
  - The `requests10h30.txt`

2. Run the tool by using the following command line instruction:  
   python main.py inputFile1.txt inputFile2.txt inputFile3.txt

   where:
   - inputFile1.txt is a `doctors` text file such as `doctors10h00.txt`
   - inputFile2.txt is a `schedule` text file such as `schedule10h00.txt`
   - inputFile3.txt is a `requests` text file such as `requests10h30.txt`

   These input files can be found within the folder `testSets`.

3. The tool will produce two new text files, incremented by 30 minutes relative to the time in the input file. In the case of the input files above, the ouput files would be:
  - `doctors10h30.txt`
  - `schedule10h30.txt`

   Running the tool with the input files in `testSets\testSet4` will raise an exception due to file name and header inconsistency in the file `requests18h30.txt`.


## Specification of the Project

The following simplifications are assumed:
- updates are made every 30 minutes;
- working hours are from 4:00 to 20:00 every day of the year, with no stopping for holidays or weekends;
- every month of every year has 30 days; 
- only daily break periods are considered; 
- doctors' weekly time off and its impact on scheduling are handled by another application.

### Doctors

In the doctors file, following the header, each line corresponds to a doctor (with each informative element separated by a comma), sorted alphabetically by the doctor's name from top to bottom. The header shows the time and date of the last update to the doctors file.

Each doctor is characterized by:
- name (e.g. Andrew Davies)
- category (from least to most experienced: 1, 2, or 3) (e.g. 1)
- daily availability for a new assistance, which corresponds to the planned completion time of their last assigned delivery (note: for new assignments, the later time between this and the header time will be used) (e.g. 11h05)
- accumulated minutes since the start of the day for assigned deliveries they have performed or will perform (e.g. 180)
- accumulated hours and minutes since the last weekly rest for assigned deliveries they have performed or will perform (e.g. 28h00)

Example of a doctor: Andrew Davies, 1, 11h05, 180, 28h00

If due to an assignment, the daily accumulated time exceeds 240 minutes (4 hours) for the first time, a 1-hour break must be added to determine when that doctor will be available again for an assistance after their daily break.

If due to an assignment, the weekly accumulated time exceeds the 40-hour threshold, that doctor's line should appear as in the following example:
Michael Owen, 3, weekly leave, 120, 40h15

### Requests

In the requests file, following the header, each line corresponds to an assistance request (with each informative element separated by a comma), ordered by arrival time. The header shows the time and date up to which the requests have been recorded, which matches the last update time of the doctors' and schedule files. 

Each request is characterized by:
- mother's name (e.g. Barbara Brooks)
- age (in years) (e.g. 28)
- wristband color (green, yellow, red) (e.g. green)
- delivery risk (low, medium, high) (e.g. high)

Example of a request: Barbara Brooks, 28, green, high

Each assistance is planned to last 20 minutes.

### Schedule

In the schedule file, following the header, each line corresponds to a scheduled assistance (with each informative element separated by a comma), ordered by ascending start time. For equal start times, lines are sorted alphabetically by the names of mothers.

Each assistance is characterized by:
- time at which the assistance is planned to start (e.g. 9h50)
- mother's name (e.g. Mary Evans)
- name of the doctor who will carry out the birth assistance (e.g. Brian Cooper)

Example of an assistance: 9h50, Mary Evans, Brian Cooper


### Output Files

#### Header

The output file header matches the input file header, updated by 30 minutes.

#### Schedule

The schedule output file has a similar structure to its input file. The differences are (1) the header time is updated (30 minutes added from input file time), and (2) newly assigned assistances are added, while the completed ones by the time the following update is made are removed.

In the schedule output file, entries are ordered by ascending starting times. For equal starting times, sorting is done by alphabetical order of mothers' names. This file also includes previously scheduled assistances from the input file starting at or after the output file's time. All newly scheduled assistances cannot occur before the output file's time. 

#### Doctors

The doctors output file has a similar structure to its input file. The differences are (1) the header time is updated (30 minutes added from input file time), and (2) for the doctors that were part of an assistance, three fields are updated: daily availability for a new assistance, accumulated minutes since the start of the day and accumulated hours and minutes since the last weekly rest.


### Assignment of requests to doctors

#### Requests

Requests must be assigned to doctors based on their earliest availability, prioritizing mothers in more urgent circumstances. The mother who is first sought for assistance will be the one with the highest risk. In case of a tie, it's the mother with the most urgent wristband color. If still tied, it's the older mother. If still tied, it's the one whose name comes first alphabetically.

#### Doctors
The doctor assigned to an assistance will be the one available first, considering that only doctors of category 2 or higher can assist in high-risk deliveries. In case of a tie, it's the doctor with the highest category. If still tied, it's the doctor with the longest time remaining before having to take a break. If still tied, it's the one whose name comes first alphabetically.

This assignment continues until reaching the maximum accumulated hours that doctor can work without weekly rest, or exceeding this limit only to finish a last service that began before reaching this limit. Otherwise, that assistance must be assigned to another doctor. If there is no other doctor able to perform it, that assistance must be redicted to another hospital network.

Assignments are made as long as assistances do not extend beyond 20h00 of that day. If it extends beyond that time, the assistance is redirected to another hospital network. Redirected assistances to another hospital network are shown as ``HHhMM, mother's name, redirected to other network``, where HHhMM is the scheduling update time. If multiple such cases exist at the same HHhMM, lines are ordered by the mothers' priority rules.


### Exception

The exception ``File head error: scope inconsistency between name and header in file <name of file>`` is raised when an input file shows inconsistency between its name and header regarding scope (doctors, schedule, requests). Such an exception is thrown for any input file where this type of inconsistency occurs.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Structure

```
birth-plan-manager/
├── classes/
  ├── Assistance.py
  ├── DataManager.py
  ├── Doctor.py
  ├── DoctorsCollection.py
  ├── Header.py
  ├── Mother.py
  ├── MothersCollection.py
  ├── Schedule.py
  └── Time.py
├── testSets/
  ├── testSet1/
    ├── doctors10h00.txt
    ├── requests10h30.txt
    └── schedule10h00.txt
  ├── testSet2/
    ├── doctors14h00.txt
    ├── requests14h30.txt
    └── schedule14h00.txt
  ├── testSet3/
    ├── doctors16h00.txt
    ├── requests16h30.txt
    └── schedule16h00.txt
  └── testSet4/
    ├── doctors18h00.txt
    ├── requests18h30.txt
    └── schedule18h00.txt
├── LICENSE
├── README.md
├── constants.py
└── main.py
