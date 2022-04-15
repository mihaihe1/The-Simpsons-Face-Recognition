# The-Simpsons-Face-Recognition

Primul pas in rezolvarea task-ului a fost generarea exemplelor pozitive si negative de dimensiunile ferestrei glisante. Am ales sa folosesc o fereastra dreptunghiulara de dimensiuni 56x64 pentru generarea exemplelor. Am incercat diverse dimensiuni pentru ferestre patratice(32x32, 64x64), insa personajele cu forma fetei dreptunghiulara(Bart, Homer) nu erau detectate corect. Pentru exemplele pozitive, am preluat setul de antrenare si am extras fetele din fisierul ce continea bounding box-urile corecte ale fetelor, redimensionandu-le la dimensiunea ferestrei mele. Pentru cele negative, am folosit tot setul de antrenare, insa am extras cate 5 patch-uri random din fiecare imagine, care nu au intersectia cu un bounding box al unei fete mai mare de 10%.

Urmatorul pas a fost extragerea descriptorilor pozitivi si negativi. Pentru aceasta am incercat extragerea descriptorilor hog folosind imaginea grayscale, dar si pastrand numai informatia importanta din imagini, culoarea galben, folosind o filtrare HSV. A doua varianta s-a dovedit castigatoare si am extras descriptorii folosind aceasta filtrare cu un dim_hog_cell=10.

Pentru a antrena un model ce va detecta daca in patch am sau nu o fata, am incercat sa antrenez un SVM liniar si unul cu kernel rbf, insa SVM-ul liniar a obtinut un scor mai mare pe configuratia mea.

In faza de detectare faciala, am ales sa maresc si micsorez imaginile intr-un while loop pana obtin diverse valori prestabilite, pentru a nu mari sau micsora inutil. Micsorarea imaginilor s-a realizat pana ajung la o poza mai mica decat fereastra glisanta(56x64), iar pentru marire am obtinut cele mai bune rezultate pentru un prag de 400x400. Pentru micsorare, am facut resize imaginii cu un scale de 0.65 la fiecare pas, iar pentru marire 1.3.

Pentru fiecare fereastra glisanta obtinuta am verificat daca prin aplicarea filtrului HSV obtin o medie ce ma asigura ca nu am o fata in patch. Media pe exemplele negative este de 30 si am ales sa folosesc media 35 pentru a exclude anumite patch-uri incorecte. De

asemenea, un alt criteriu de eliminare al unui patch este de a verifica ca scorul acelui patch este pozitiv.

Aceasta solutie a obtinut un mAP de 68% pe setul de validare.

Rezolvarea task-ului 2 a implicat folosirea unui CNN(model.py, cod “imprumutat” de la rezolvarea temei primita anul trecut la IA) cu 5 clase, corespunzatoare fiecarui personaj + unknown. Am folosit aceeasi idee de la task-ul 1, insa cand gasesc o fereastra ce contine o fata voi apela metoda predict a modelului CNN, pentru a vedea din ce clasa face parte fata din fereastra glisanta. Daca predictia corespunde clasei unknown, ignor aceasta fereastra. Folosind acest clasificator am obtinut media mAP de 31% pe setul de validare
