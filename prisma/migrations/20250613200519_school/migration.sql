-- CreateEnum
CREATE TYPE "Status" AS ENUM ('encours', 'terminer');

-- CreateTable
CREATE TABLE "Student" (
    "id" SERIAL NOT NULL,
    "nom" TEXT NOT NULL,
    "prenom" TEXT NOT NULL,
    "biographie" TEXT NOT NULL,
    "mail" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updateAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Student_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Teacher" (
    "id" SERIAL NOT NULL,
    "nom" TEXT NOT NULL,
    "prenom" TEXT NOT NULL,
    "biographie" TEXT NOT NULL,
    "mail" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updateAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Teacher_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Section" (
    "id" SERIAL NOT NULL,
    "CoursId" INTEGER NOT NULL,
    "Titre" TEXT NOT NULL,
    "contenu" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updateAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Section_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Cours" (
    "id" SERIAL NOT NULL,
    "auteurId" INTEGER NOT NULL,
    "titre" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updateAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Cours_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SuiviCours" (
    "id" SERIAL NOT NULL,
    "coursId" INTEGER NOT NULL,
    "studentId" INTEGER NOT NULL,
    "statut" "Status" NOT NULL,
    "debut" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "fin" TIMESTAMP(3),

    CONSTRAINT "SuiviCours_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "_StudentCours" (
    "A" INTEGER NOT NULL,
    "B" INTEGER NOT NULL
);

-- CreateIndex
CREATE UNIQUE INDEX "Student_mail_key" ON "Student"("mail");

-- CreateIndex
CREATE UNIQUE INDEX "Teacher_mail_key" ON "Teacher"("mail");

-- CreateIndex
CREATE UNIQUE INDEX "_StudentCours_AB_unique" ON "_StudentCours"("A", "B");

-- CreateIndex
CREATE INDEX "_StudentCours_B_index" ON "_StudentCours"("B");

-- AddForeignKey
ALTER TABLE "Section" ADD CONSTRAINT "Section_CoursId_fkey" FOREIGN KEY ("CoursId") REFERENCES "Cours"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Cours" ADD CONSTRAINT "Cours_auteurId_fkey" FOREIGN KEY ("auteurId") REFERENCES "Teacher"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "SuiviCours" ADD CONSTRAINT "SuiviCours_coursId_fkey" FOREIGN KEY ("coursId") REFERENCES "Cours"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "SuiviCours" ADD CONSTRAINT "SuiviCours_studentId_fkey" FOREIGN KEY ("studentId") REFERENCES "Student"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_StudentCours" ADD CONSTRAINT "_StudentCours_A_fkey" FOREIGN KEY ("A") REFERENCES "Cours"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_StudentCours" ADD CONSTRAINT "_StudentCours_B_fkey" FOREIGN KEY ("B") REFERENCES "Student"("id") ON DELETE CASCADE ON UPDATE CASCADE;
