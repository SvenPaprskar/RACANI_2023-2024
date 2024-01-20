#include <stdio.h>
#include <math.h>
#include <GL/freeglut.h>
#include <stdlib.h>
#include <time.h>

#define BROJ_CESTICA 10000
#define VREMENSKA_KONST 0.9f
#define KONST2 0.0015f
#define KONST 0.0002f

void osvjezi();
void pocetno();
void vrijeme(int v);
void prikaz();
void promjena(int sirina, int visina);

typedef struct {
    float zivot, sila_na_cesticu, masa, brzina_u_x_smjeru, brzina_u_y_smjeru, x_koordinata, y_koordinata;
} Cst;

int p;

Cst cst[BROJ_CESTICA];

int main(int argc, char *argv[]) {
    printf("Tocka privlacenja? 1 za DA i 0 za NE: ");
    scanf("%d", &p);
    srand((unsigned int) time(NULL));
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowSize(1300, 1200);
    glutCreateWindow("Sustav_cestica");
    glPointSize(5.0);
    glutDisplayFunc(prikaz);
    glutReshapeFunc(promjena);
    pocetno();
    glutTimerFunc(0, vrijeme, 0);
    glutMainLoop();
    return 0;
}

void osvjezi() {
    float privlacenje_u_x_smjeru = 0.02f;
    float privlacenje_u_y_smjeru = 0.02f;
    int z;
    float sila_u_y_smjeru, ubrzanje;
    for (z = 0; z < BROJ_CESTICA; z++) {
        if (cst[z].zivot > 0.0f) {
                if(p) {
                        float razlika_po_x = privlacenje_u_x_smjeru - cst[z].x_koordinata;
                        float razlika_po_y = privlacenje_u_y_smjeru - cst[z].y_koordinata;
                        float udaljenost = pow(razlika_po_x, 2) + pow(razlika_po_y, 2);
                        float jacina_privlacenja_x = (razlika_po_x / udaljenost) * KONST;
                        float jacina_privlacenja_y = (razlika_po_y / udaljenost) * KONST;
                        cst[z].brzina_u_x_smjeru += jacina_privlacenja_x;
                        cst[z].brzina_u_y_smjeru += jacina_privlacenja_y;
                }
            sila_u_y_smjeru = cst[z].sila_na_cesticu + cst[z].masa * KONST2;
            ubrzanje = sila_u_y_smjeru / cst[z].masa;
            cst[z].brzina_u_y_smjeru -= ubrzanje * VREMENSKA_KONST;
            cst[z].x_koordinata += cst[z].brzina_u_x_smjeru * VREMENSKA_KONST;
            cst[z].y_koordinata += cst[z].brzina_u_y_smjeru * VREMENSKA_KONST;
            cst[z].zivot -= 0.02322f;
        } else {
            cst[z].x_koordinata = 0.f;
            cst[z].sila_na_cesticu = ((float)(rand() % 1000) / 1000.f) * 0.00143f;
            cst[z].brzina_u_x_smjeru = ((float)(rand() % 1000) / 1000.f - 0.5f) * 0.081f;
            cst[z].masa = ((float)(rand() % 1000) / 1000.f) * 4.f;
            cst[z].brzina_u_y_smjeru = ((float)(rand() % 1000) / 1000.f) * 0.063f;
            cst[z].zivot = (float)(rand() % 1000) / 1000.f;
            cst[z].y_koordinata = 0.f;
        }
    }
}

void pocetno() {
    for (int k = 0; k < BROJ_CESTICA; k++) {
            cst[k].sila_na_cesticu = ((float)(rand() % 1000) / 1000.f) * 0.00143f;
            cst[k].brzina_u_x_smjeru = ((float)(rand() % 1000) / 1000.f - 0.5f) * 0.081f;
            cst[k].masa = ((float)(rand() % 1000) / 1000.f) * 4.f;
            cst[k].brzina_u_y_smjeru = ((float)(rand() % 1000) / 1000.f) * 0.063f;
            cst[k].x_koordinata = 0.f;
            cst[k].zivot = (float)(rand() % 1000) / 1000.f;
            cst[k].y_koordinata = 0.f;
        }
    }

void vrijeme(int v) {
    osvjezi();
    glutPostRedisplay();
    glutTimerFunc(16, vrijeme, 0);
}

void prikaz() {
    int j;
    glColor3f(1, 0, 0);
    glClear(GL_COLOR_BUFFER_BIT);
    glLoadIdentity();
    glBegin(GL_POINTS);
    for (j = 0; j < BROJ_CESTICA; j++) {
        if (cst[j].zivot > 0.f) {
            glVertex2f(cst[j].x_koordinata, cst[j].y_koordinata);
        }
    }
    glEnd();
    glutSwapBuffers();
}

void promjena(int sirina, int visina) {
    glViewport(0, 0, sirina, visina);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(-2, 2, -2, 2, -2, 2);
    glMatrixMode(GL_MODELVIEW);
}
