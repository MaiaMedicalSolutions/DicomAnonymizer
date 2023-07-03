# Dicom Anonymizer Repository

### ENGLISH
This repository contains the source 
code for a DICOM anonymization algorithm based on the latest standard (2023a). 
The code is developed for the MAIA (Medical AI Assistant) project.

DICOM is the standard for 
transmitting, storing, and sharing medical images and related information. 
However, it is crucial to ensure patient privacy and confidentiality when working 
with DICOM data. This repository provides an anonymization solution that enables 
the user to remove identifying information from DICOM files, making them suitable for 
research, analysis, and sharing while protecting patient privacy.

#### Repository Structure
* documentations/: This folder contains the exported standard files from the official 
DICOM website (https://www.dicomstandard.org/). These files serve as a reference 
for understanding the DICOM standard and implementing the anonymization algorithm.
* data/: This folder contains JSON files that encode the actions to be performed 
on specific DICOM tags during the anonymization process. These files define the
rules and instructions for handling different types of data.
* src/: This folder contains the source code of the DICOM anonymization algorithm. 
It includes the necessary modules and functions to process DICOM files, remove 
identifying information, and generate anonymized versions of the files.

### HUNGARIAN
Ez a repository egy DICOM anonimizáló algoritmus forráskódját tartalmazza, 
amely a legújabb szabványon (2023a) alapul. 
A kódot a MAIA (Medical AI Assistant) projekthez fejlesztettük.

A DICOM fájl formátum orvosi képek és kapcsolódó információk továbbítására, tárolására 
és megosztására szolgál. Kulcsfontosságú a betegek magánéletének 
és bizalmasságának biztosítása a DICOM-adatokkal való munka során. Ez a repository 
anonimizálási megoldást kínál, amely lehetővé teszi a felhasználó számára, hogy
eltávolítsa a betegegek/alanyok azonosítására használható információkat a 
DICOM-fájlokból, így alkalmassá teszi azokat
kutatásra, elemzésre és megosztásra, miközben védi a betegek adatait.

#### Repository szerkezet
* documentations/: Ez a mappa tartalmazza a hivatalos weboldalról (https://www.dicomstandard.org/) exportált szabványos 
anonimizáló megoldás dokumentációját. Ezek a fájlok referenciaként szolgálnak
a DICOM szabvány megértéséhez és az anonimizálási algoritmus implementálásához.
* data/: Ez a mappa JSON-fájlokat tartalmaz, amelyek kódolják a végrehajtandó műveleteket (`actions`) az
adott DICOM tageken. Ezek a fájlok határozzák meg a szabályokat és utasításokat a különböző típusú adatok kezelésére.
* src/: Ez a mappa tartalmazza a DICOM anonimizálási algoritmus forráskódját.
Tartalmazza a DICOM fájlok feldolgozásához és eltávolításához szükséges modulokat és funkciókat
azonosítási információkat, és létrehozza a fájlok névtelen verzióit.