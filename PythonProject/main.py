import sys
from xmlrpc.client import FastParser

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem

from login_ui import Ui_login
from recupera_ui import Ui_recuperapassword
from mainwindow import Ui_MainWindow
from adminwindow_ui import Ui_AdminWindow
import mysql.connector
from datetime import datetime, date

#python -m PyQt6.uic.pyuic -o recupera_ui.py recuperaPassword.ui
#python -m PyQt6.uic.pyuic -o login_ui.py login.ui
#python -m PyQt6.uic.pyuic -o mainwindow.py mainwindow.ui
#python -m PyQt6.uic.pyuic -o adminwindow_ui.py adminwindow.ui

class AdminWindow(QtWidgets.QMainWindow, Ui_AdminWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnDipendentiAdm.clicked.connect(lambda: self.mainFrame.setCurrentIndex(0))
        self.btnMagazziniAdm.clicked.connect(lambda: self.mainFrame.setCurrentIndex(7))
        self.btnProdottiAdm.clicked.connect(lambda: self.mainFrame.setCurrentIndex(3))
        self.btnMansioniAdm.clicked.connect(lambda: self.mainFrame.setCurrentIndex(1))
        self.btnColtureAdm.clicked.connect(lambda: self.mainFrame.setCurrentIndex(2))
        self.btnTerreniAdm.clicked.connect(lambda: self.mainFrame.setCurrentIndex(5))

        self.btnDipendentiAdm.clicked.connect(self.caricaUtenti)
        self.cmbSeleziona.currentIndexChanged.connect(self.cambioUtente)
        self.btnCreaModAccount.clicked.connect(self.creaUtente)
        self.btnRimAccount.clicked.connect(self.rimuoviUtente)

        self.btnMagazziniAdm.clicked.connect(self.riempiMagazzini)
        self.btnAggMagazzino.clicked.connect(self.aggMagazz)
        self.btnRimMagazz.clicked.connect(self.rimuoviMagazz)

        self.btnColtureAdm.clicked.connect(self.riempiColture)
        self.btnRimColtura.clicked.connect(self.rimuoviColtura)
        self.btnAggColtura.clicked.connect(self.aggiungiColtura)

        self.btnMansioniAdm.clicked.connect(self.caricaMansioni)
        self.btnMansioniAdm.clicked.connect(self.caricaUtentiMansione)
        self.cmbSelezionaMans.currentIndexChanged.connect(self.selezionaMansione)
        self.btnCreaModMans.clicked.connect(self.creaModificaMansione)
        self.btnRimMans.clicked.connect(self.rimuoviMansione)
        self.btnAssMans.clicked.connect(self.assegnaMansione)

        self.btnTerreniAdm.clicked.connect(self.caricaTerreni)
        self.buttonAggiungiTerreno.clicked.connect(self.aggiungiTerreno)
        self.buttonRimuoviTerreno.clicked.connect(self.rimuoviTerreno)

        self.btnProdottiAdm.clicked.connect(self.caricaProdotti)
        self.btnAggProd.clicked.connect(self.aggiungiProdotto)
        self.btnRimProd.clicked.connect(self.rimuoviProdotto)

    import mysql.connector

    def rimuoviTerreno(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="agrilogic"
            )
            cursor = conn.cursor()
            idTerr = self.comboSelezTerrRim.currentText()

            try:
                # Controlla l’ultima riga nella tabella coltiva per quel tereeno
                cursor.execute(
                    "SELECT dataRaccolta FROM coltiva WHERE id_terreno = %s ORDER BY id DESC LIMIT 1;",
                    (idTerr,)
                )
                result = cursor.fetchone()

                # Se esiste e la raccolta è completa fa questo
                if result is not None and result[0] is None:
                    QMessageBox.warning(self, "Errore",
                                        "Non puoi eliminare il terreno: la coltura non è ancora stata raccolta.")


                else:
                    # Elimina prima dalla tabella dell'associazione
                    cursor.execute("DELETE FROM coltiva WHERE id_terreno = %s", (idTerr,))
                    # elimina dalla tabella terreno
                    cursor.execute("DELETE FROM terreno WHERE id = %s", (idTerr,))
                    conn.commit()  # Applica le modifiche
                    QMessageBox.information(self, "Eliminazione riuscita", "Il terreno è stato eliminato con successo.")

            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Errore", f"Errore durante l’accesso al database:\n{err}")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Errore", f"Errore durante la connessione al database:\n{err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        self.caricaTerreni()

    def aggiungiTerreno(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="agrilogic"
            )
            cursor = conn.cursor()

            codP = self.txtCodiceP.text().strip()
            nomeP = self.txtNomeP.text().strip()

            # Inserimento prodotto
            cursor.execute("INSERT INTO terreno(livelloirrigazione, stato) VALUES (100,'VUOTO')")
            conn.commit()
            QMessageBox.information(self, "Successo", "Terreno aggiunto con successo")
            self.btnRimProd.setEnabled(True)


        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Errore", f"Errore durante il salvataggio del terreno:\n{err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        self.caricaTerreni()

    def caricaTerreni(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="agrilogic"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM terreno")
            result = cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Errore MySQL: {e}")
            return
        finally:
            cursor.close()
            conn.close()

        if not result:
            self.buttonRimuoviTerreno.setEnabled(False)  # disattiva il pulsante se lista vuota
        else:
            self.buttonRimuoviTerreno.setEnabled(True)  # attiva se ci sono terreni

        cursor.close()
        conn.close()

        self.comboSelezTerrRim.blockSignals(True)
        self.comboSelezTerrRim.clear()

        # Conversione a stringhe per evitare errori in addItems
        terreni = [str(row[0]) for row in result]
        self.comboSelezTerrRim.addItems(terreni)

        self.comboSelezTerrRim.blockSignals(False)

        # Seleziona il primo elemento di default
        if terreni:  # Solo se la lista non è vuota lo fa
            self.comboSelezTerrRim.setCurrentIndex(0)

    def rimuoviProdotto(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="agrilogic"
            )
            cursor = conn.cursor()
            selected_task = self.cmbRimProd.currentText()
            codice = selected_task.split('-')[0].strip()  # "1"

            cursor.execute("SELECT id FROM prodotto WHERE codice = %s", (codice,))
            result = cursor.fetchone()

            if result is None:
                QMessageBox.warning(self, "Errore", f"Nessun prodotto trovato con codice {codice}.")
            else:
                idProdotto = result[0]
                cursor.execute("DELETE FROM contiene WHERE id_prodotto = %s", (idProdotto,))
                conn.commit()
                cursor.execute("DELETE FROM prodotto WHERE id = %s", (idProdotto,))
                conn.commit()
                QMessageBox.information(self, "Successo",
                                        f"Prodotto con codice {codice} eliminato dal magazzino.")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Errore", f"Errore durante l'eliminazione del prodotto:\n{err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        self.caricaProdotti()

    def aggiungiProdotto(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="agrilogic"
            )
            cursor = conn.cursor()

            codP = self.txtCodiceP.text().strip()
            nomeP = self.txtNomeP.text().strip()

            # Controllo campi vuoti
            if codP == "" or nomeP == "":
                QMessageBox.critical(self, "Errore", "Inserire sia codice che il nome del prodotto")
                return

            # Controllo se il prodotto già esiste
            cursor.execute("SELECT * FROM prodotto WHERE codice = %s", (codP,))
            result = cursor.fetchone()

            if result is None:
                # Inserimento prodotto
                cursor.execute("INSERT INTO prodotto (codice, nome) VALUES (%s, %s)", (codP, nomeP))
                conn.commit()
                QMessageBox.information(self, "Successo", "Prodotto aggiunto con successo")
                self.btnRimProd.setEnabled(True)

            else:
                QMessageBox.warning(self, "Attenzione", "Prodotto già esistente con questo codice")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Errore", f"Errore durante il salvataggio del prodotto:\n{err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        self.caricaProdotti()

    def caricaProdotti(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="agrilogic"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT codice, nome FROM prodotto")
            result = cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Errore MySQL: {e}")
            return
        finally:
            cursor.close()
            conn.close()

        if not result:
            self.btnRimProd.setEnabled(False)  # disattiva il pulsante se e lista vuota
        else:
            self.btnRimProd.setEnabled(True)  # attiva se ci sono prodotti

        cursor.close()
        conn.close()

        self.cmbRimProd.blockSignals(True)
        self.cmbRimProd.clear()

        # Usa None in prima posizione per 'Nuovo'
        prodotti = [f"{row[0]} - {row[1]}" for row in result]

        self.cmbRimProd.addItems(prodotti)
        self.cmbRimProd.blockSignals(False)

        # Seleziona il primo elemento di default
        self.cmbRimProd.setCurrentIndex(0)

    def rimuoviMansione(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="agrilogic"
            )
            cursor = conn.cursor()
            selected_task = self.cmbSelezionaMans.currentText()
            idMans = selected_task.split('-')[0].strip()  # "1"
            try:
                cursor.execute("DELETE FROM mansione WHERE id = %s", (idMans,))
                conn.commit()
            except mysql.connector.Error as e:
                if "foreign key constraint fails" in str(e):
                    QMessageBox.warning(self, "Errore", "Non puoi eliminare la mansione: è stata utilizzata.")
                else:
                    QMessageBox.information(self, "Eliminazione riuscita", "Mansione eliminata con successo")


        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Errore", f"Errore durante il salvataggio della mansione:\n{err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        self.caricaMansioni()

    def assegnaMansione(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="agrilogic"
            )
            cursor = conn.cursor()

            # Estrai id utente e id mansione dalle combo box
            selected_text = self.cmbSelUtAss.currentText()
            idUser = selected_text.split('-')[0].strip()

            selected_task = self.cmbSelMansAss.currentText()
            idMans = selected_task.split('-')[0].strip()

            # Controlla se l'assegnazione esiste gia
            query_check = "SELECT 1 FROM assegna WHERE id_utente = %s AND id_mansione = %s"
            cursor.execute(query_check, (idUser, idMans))
            result = cursor.fetchone()

            if result is None:
                query_insert = "INSERT INTO assegna (id_utente, id_mansione) VALUES (%s, %s)"
                cursor.execute(query_insert, (idUser, idMans))
                QMessageBox.information(self, "Successo", "Mansione assegnata.")
            else:
                query_delete = "DELETE FROM assegna WHERE id_utente = %s AND id_mansione = %s"
                cursor.execute(query_delete, (idUser, idMans))
                QMessageBox.information(self, "Successo", "Mansione rimossa.")

            conn.commit()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Errore", f"Errore durante il salvataggio della mansione:\n{err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def caricaUtentiMansione(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="agrilogic"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, email FROM user WHERE ruolo='dipendente'")
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        self.cmbSelUtAss.blockSignals(True)
        self.cmbSelUtAss.clear()

        # Usa None in prima posizione per 'Nuovo'
        self.ids = [None] + [row[0] for row in result]

        utenti = [f"{row[0]} - {row[1]}" for row in result]

        self.cmbSelUtAss.addItems(utenti)
        self.cmbSelUtAss.blockSignals(False)

        # Seleziona il primo elemento di default
        self.cmbSelUtAss.setCurrentIndex(0)

    def creaModificaMansione(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="agrilogic"
            )
            cursor = conn.cursor()
            tipo = ""
            stato = ""
            query = ""

            if self.cmbTipoMans.currentIndex() == 0:
                tipo = "FISSA"
            elif self.cmbTipoMans.currentIndex() == 1:
                tipo = "GIORNALIERA"

            if self.cmbStatoMans.currentIndex() == 0:
                stato = "IN_ATTESA"
            elif self.cmbStatoMans.currentIndex() == 1:
                stato = "IN_CORSO"
            elif self.cmbStatoMans.currentIndex() == 2:
                stato = "COMPLETATA"

            descrizione = self.txtDesc.toPlainText()

            if self.cmbSelezionaMans.currentIndex() == 0:
                query = "INSERT INTO mansione (tipo, stato, descrizione) VALUES (%s, %s, %s)"
                cursor.execute(query, (tipo, stato, descrizione))
                self.btnRimMans.setEnabled(True)

            else:
                selected_text = self.cmbSelezionaMans.currentText()
                id = selected_text.split('-')[0].strip()
                query = "UPDATE mansione SET tipo=%s, stato=%s, descrizione=%s WHERE id=%s"
                cursor.execute(query, (tipo, stato, descrizione, id))

            conn.commit()
            QMessageBox.information(self, "Operazione riuscita", "Mansione salvata con successo")

            # Reset dei campi
            self.cmbTipoMans.setCurrentIndex(0)
            self.cmbStatoMans.setCurrentIndex(0)
            self.cmbSelezionaMans.setCurrentIndex(0)
            self.txtDesc.clear()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Errore", f"Errore durante il salvataggio della mansione:\n{err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
        self.caricaMansioni()

    def selezionaMansione(self):

        if self.cmbTipoMans.currentIndex() == 0:
            self.cmbTipoMans.setCurrentIndex(0)
            self.cmbStatoMans.setCurrentIndex(0)
            self.txtDesc.clear()
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="agrilogic"
        )
        cursor = conn.cursor()
        selected_text = self.cmbSelezionaMans.currentText()
        id = selected_text.split('-')[0].strip()  # "1"

        cursor.execute("SELECT tipo, descrizione, stato FROM mansione WHERE id=%s", (id,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        if result:
            tipo, descrizione, stato = result[0]

            if tipo == "Fissa":
                self.cmbTipoMans.setCurrentIndex(0)
            elif tipo == "Giornaliera":
                self.cmbTipoMans.setCurrentIndex(1)

            self.txtDesc.setText(descrizione)

            if stato == "In Attesa":
                self.cmbStatoMans.setCurrentIndex(0)
            elif stato == "In Corso":
                self.cmbStatoMans.setCurrentIndex(1)
            elif stato == "Completata":
                self.cmbStatoMans.setCurrentIndex(2)

    def caricaMansioni(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="agrilogic"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, descrizione FROM mansione ORDER BY id ASC")
        result = cursor.fetchall()
        if not result:
            self.btnRimMans.setEnabled(False)  # disattiva il pulsante se lista vuota
        else:
            self.btnRimMans.setEnabled(True)  # attiva se ci sono mansioni

        cursor.close()
        conn.close()

        self.cmbSelezionaMans.blockSignals(True)
        self.cmbSelezionaMans.clear()
        self.cmbSelMansAss.blockSignals(True)
        self.cmbSelMansAss.clear()

        # Usa None in prima posizione per 'Nuovo'
        self.ids = [None] + [row[0] for row in result]

        mansioni = [f"{row[0]} - {row[1]}" for row in result]

        self.cmbSelezionaMans.addItem("Nuovo")
        self.cmbSelezionaMans.addItems(mansioni)
        self.cmbSelMansAss.blockSignals(False)
        self.cmbSelMansAss.addItems(mansioni)
        self.cmbSelezionaMans.blockSignals(False)

        # Seleziona il primo elemento di default
        self.cmbSelezionaMans.setCurrentIndex(0)


        self.cmbTipoMans.clear()
        self.cmbTipoMans.addItem("Fissa")
        self.cmbTipoMans.addItem("Giornaliera")

        self.cmbStatoMans.clear()
        self.cmbStatoMans.addItem("In Attesa")
        self.cmbStatoMans.addItem("In Corso")
        self.cmbStatoMans.addItem("Completata")

    def aggiungiColtura(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="agrilogic"
            )
            cursor = conn.cursor()

            nome = self.txtAggiungiColtura.text().strip()  # Rimuove spazi
            if nome == "":
                QMessageBox.warning(self, "Errore", "Inserire un nome valido per la coltura.")

                return
            # Controllo se la coltura gia esiste
            cursor.execute("SELECT * FROM coltura WHERE nome = %s", (nome,))
            result = cursor.fetchone()

            if result is None:
                # Inserimento prodotto
                cursor.execute("INSERT INTO coltura (nome) VALUES (%s)", (nome,))
                conn.commit()
                QMessageBox.information(self, "Successo", "Coltura aggiunta con successo")
                self.txtAggiungiColtura.setText("")

            self.btnRimColtura.setEnabled(True)

            # Reset campi numerici
            self.numAggMagCap.setValue(0)
            self.numAggMagMet.setValue(0)

            # Ricarica lista colture
            self.riempiColture()

        except mysql.connector.Error as e:
            print(f"Errore DB: {e}")
            return

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def rimuoviColtura(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="agrilogic"
            )
            cursor = conn.cursor()

            nome = self.cmbRimuoviColtura.currentText()

            try:
                # Controlla se ci sono colture piantate (non raccolte) con quel nome
                cursor.execute("""SELECT coltiva.*
                                  FROM coltiva
                                           JOIN coltura ON coltiva.id_coltura = coltura.id
                                  WHERE coltura.nome = %s
                                    AND coltiva.dataRaccolta IS NULL""", (nome,))
                result = cursor.fetchall()

                if result:  # Se ci sono righe la coltura è piantata, non si può togliere
                    QMessageBox.information(self, "Errore", "La coltura è ancora piantata, non può essere eliminata.")
                else:
                    cursor.execute("DELETE FROM coltura WHERE nome = %s", (nome,))
                    conn.commit()
                    QMessageBox.information(self, "Eliminata", "La coltura è stata rimossa con successo.")

            except mysql.connector.Error as e:
                if "foreign key constraint fails" in str(e):
                    QMessageBox.warning(self, "Errore", "Non puoi eliminare la coltura: è stata utilizzata.")
                else:
                    QMessageBox.critical(self, "Errore", f"Errore durante l'eliminazione:\n{e}")

            # Aggiorna combo box
            self.riempiColture()

        except mysql.connector.Error as e:
            print(f"Errore DB: {e}")
            return

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    def riempiColture(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="agrilogic"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM coltura")
            result = cursor.fetchall()
            if not result:
                self.btnRimColtura.setEnabled(False)  # disattiva il pulsante se lista vuota
            else:
                self.btnRimColtura.setEnabled(True)  # attiva se ci sono prodotti

        except mysql.connector.Error as e:
            print(f"Errore DB: {e}")
            return

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

        self.nomi = [row[0] for row in result]

        self.cmbRimuoviColtura.clear()
        self.cmbRimuoviColtura.addItems(self.nomi)
        if self.nomi:
            self.cmbRimuoviColtura.setCurrentIndex(0)

    def riempiMagazzini(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="agrilogic"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM magazzino")
            result = cursor.fetchall()
            if not result:
                self.btnRimMagazz.setEnabled(False)  # disattiva il pulsante se lista vuota
            else:
                self.btnRimMagazz.setEnabled(True)  # attiva se ci sono magazzini
        except mysql.connector.Error as e:
            print(f"Errore DB: {e}")
            return
        finally:
            cursor.close()
            conn.close()

        self.ids = [row[0] for row in result]

        self.cmbRimMagazz.clear()
        self.cmbRimMagazz.addItems([str(id_) for id_ in self.ids])  # conversione qui
        if self.ids:
            self.cmbRimuoviColtura.setCurrentIndex(0)

    def rimuoviMagazz(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="agrilogic"
            )
            cursor = conn.cursor()

            magazzino = int(self.cmbRimMagazz.currentText())

            try:
                cursor.execute("DELETE FROM magazzino WHERE id = %s", (magazzino,))
                conn.commit()
            except mysql.connector.Error as e:
                if "foreign key constraint fails" in str(e):
                    QMessageBox.warning(self, "Errore", "Non puoi eliminare il magazzino: contiene prodotti.")
                else:
                    QMessageBox.information(self, "Eliminazione riuscita", "Magazzino eliminato con successo")
            # Conferma le modifiche
            conn.commit()
            self.riempiMagazzini()


        except mysql.connector.Error as e:
            print(f"Errore DB: {e}")
            return

        finally:
            # Chiudi solo se esistono
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()
        self.riempiMagazzini()

    def aggMagazz(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="agrilogic"
            )
            cursor = conn.cursor()

            capienza = self.numAggMagCap.value()
            metratura = self.numAggMagMet.value()

            query = "INSERT INTO magazzino (capienza, metratura) VALUES (%s, %s)"
            cursor.execute(query, (capienza, metratura))

            # Conferma le modifiche
            conn.commit()
            QMessageBox.information(self, "Inserimento riuscito", "Magazzino inserito con successo")
            self.btnRimMagazz.setEnabled(True)

            self.numAggMagCap.setValue(0)
            self.numAggMagMet.setValue(0)

            self.riempiMagazzini()

        except mysql.connector.Error as e:
            print(f"Errore DB: {e}")
            return

        finally:
            # Chiudi solo se esistono
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()

        self.riempiMagazzini()

    def caricaUtenti(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="agrilogic"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, email FROM user ORDER BY id ASC")
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        self.cmbSeleziona.blockSignals(True)
        self.cmbSeleziona.clear()

        # Usa None in prima posizione per 'Nuovo'
        self.ids = [None] + [row[0] for row in result]

        utenti = [f"{row[0]} - {row[1]}" for row in result]

        self.cmbSeleziona.addItem("Nuovo")
        self.cmbSeleziona.addItems(utenti)
        self.cmbSeleziona.blockSignals(False)

        # Seleziona il primo elemento di default
        self.cmbSeleziona.setCurrentIndex(0)

        self.cmbRuoloCreaAccount.clear()
        self.cmbRuoloCreaAccount.addItem("Utente")
        self.cmbRuoloCreaAccount.addItem("Amministratore")

    def cambioUtente(self, index):
        if index == 0:
            # Nuovo utente: pulisci i campi
            self.txtNomeCreaAccount.clear()
            self.txtCognomeCreaAccount.clear()
            self.txtEmailCreaAccount.clear()
            self.txtPasswordCreaAccount.clear()
            self.cmbRuoloCreaAccount.setCurrentIndex(0)
            return

        selectedUser = self.cmbSeleziona.currentText()
        emailUser = selectedUser.split('-')[1].strip()  # email

        if emailUser == mailUtente:
            self.btnRimAccount.setEnabled(False)
        else:
            self.btnRimAccount.setEnabled(True)

        # Selezionato utente esistente
        user_id = self.ids[index]
        if user_id is None:
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="agrilogic"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT nome, cognome, email, ruolo FROM user WHERE id = %s", (user_id,))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()

            if user_data:
                self.txtNomeCreaAccount.setText(user_data[0])
                self.txtCognomeCreaAccount.setText(user_data[1])
                self.txtEmailCreaAccount.setText(user_data[2])

                if user_data[3] == "amministratore":
                    self.cmbRuoloCreaAccount.setCurrentIndex(1)
                else:
                    self.cmbRuoloCreaAccount.setCurrentIndex(0)

                self.txtPasswordCreaAccount.clear()  # non mostrare la password salvata per sicurezza

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Errore database", f"Errore nel caricamento utente:\n{e}")

    def rimuoviUtente(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="agrilogic"
            )
            cursor = conn.cursor()
            selected_task = self.cmbSeleziona.currentText()
            idUser = selected_task.split('-')[0].strip()  # "1"

            try:
                cursor.execute("DELETE FROM user WHERE id = %s", (idUser,))
                conn.commit()
            except mysql.connector.Error as e:
                if "foreign key constraint fails" in str(e):
                    QMessageBox.warning(self, "Errore", "Non puoi eliminare l'utente: è presente altrove.")
                else:
                    QMessageBox.information(self, "Eliminazione riuscita", "Utente eliminato con successo")


        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Errore", f"Errore durante l'eliminazione del prodotto:\n{err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        self.caricaProdotti()

    def creaUtente(self):
        index = self.cmbSeleziona.currentIndex()

        nome = self.txtNomeCreaAccount.text().strip()
        cognome = self.txtCognomeCreaAccount.text().strip()
        email = self.txtEmailCreaAccount.text().strip()
        password = self.txtPasswordCreaAccount.text().strip()
        ruolo = self.cmbRuoloCreaAccount.currentText()  # 0 = dipendente, 1 = amministratore

        if not nome or not cognome or not email:
            QMessageBox.warning(self, "Errore", "Compila almeno nome, cognome ed email.")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="agrilogic"
            )
            cursor = conn.cursor()

            if index == 0:
                if not password:
                    QMessageBox.warning(self, "Errore", "La password è obbligatoria per un nuovo utente.")
                    return

                # Controllo se il prodotto già esiste
                cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
                result = cursor.fetchone()

                if result is None:
                    # Inserimento utente
                    cursor.execute(

                        "INSERT INTO user (nome, cognome, email, password, ruolo) VALUES (%s, %s, %s, %s, %s)",
                        (nome, cognome, email, password, ruolo)
                    )
                    conn.commit()
                    QMessageBox.information(self, "Successo", "Utente aggiunto con successo")
                    self.btnRimAccount.setEnabled(True)
                else:
                    QMessageBox.information(self, "Errore", "Utente già esistente.")

            else:
                user_id = self.ids[index]  # index è >= 1, quindi id valido

                cursor.execute(
                    "UPDATE user SET nome=%s, cognome=%s, email=%s, ruolo=%s WHERE id=%s",
                    (nome, cognome, email, ruolo, user_id)
                )

                if password:
                    cursor.execute(
                        "UPDATE user SET password=%s WHERE id=%s",
                        (password, user_id)
                    )

                QMessageBox.information(self, "Successo", "Utente aggiornato correttamente.")

                conn.commit()
                cursor.close()
                conn.close()

            self.caricaUtenti()
            self.cmbSeleziona.setCurrentIndex(0)

            self.txtNomeCreaAccount.clear()
            self.txtCognomeCreaAccount.clear()
            self.txtEmailCreaAccount.clear()
            self.txtPasswordCreaAccount.clear()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Errore database", f"Errore durante il salvataggio:\n{e}")

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnMagazzino.clicked.connect(lambda: self.mainFrame.setCurrentIndex(1))
        self.btnMagazzino.clicked.connect(self.caricamento_magazzino)
        self.btnImm.clicked.connect(self.immagazzina)
        self.btnTerreni.clicked.connect(lambda: self.mainFrame.setCurrentIndex(2))
        self.btnMansioni.clicked.connect(lambda: self.mainFrame.setCurrentIndex(0))
        self.btnTerreni.clicked.connect(self.caricamento_terreni)
        self.comboTerreni.currentIndexChanged.connect(self.irrigazione_terreni)
        self.btnIrriga.clicked.connect(self.irriga_campo)
        self.btnSemina.clicked.connect(self.semina_terreno)
        self.btnRaccolta.clicked.connect(self.raccolta_terreno)
        self.btnImpostazioni.clicked.connect(lambda: self.mainFrame.setCurrentIndex(3))
        self.btnModificaPassDipendente.clicked.connect(self.modifica_credenziali)
        self.btnSemina.clicked.connect(self.semina_terreno)
        self.btnMansioni.clicked.connect(self.riempi_combo_mansioni)
        self.cmbSelMans.currentIndexChanged.connect(self.modifica_combo_mansioni)
        self.btnAggStatMans.clicked.connect(self.modifica_stato_mansione)
        self.btnEliminaRecord.clicked.connect(self.elimina_riga_selezionata)

    def elimina_riga_selezionata(self):
        selected_items = self.tblProdScad.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, "Nessuna selezione", "Seleziona una riga da eliminare.")
            return
        riga = selected_items[0].row()
        try:
            id_magazzino = int(self.tblProdScad.item(riga, 0).text())
            nome_prodotto = self.tblProdScad.item(riga, 1).text()
            data_scadenza = self.tblProdScad.item(riga, 2).text()  # formato 'YYYY-MM-DD'
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore nella lettura della riga: {e}")
            return
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="agrilogic"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM prodotto WHERE nome = %s", (nome_prodotto,))
            result = cursor.fetchone()
            if not result:
                QMessageBox.critical(self, "Errore", "ID prodotto non trovato.")
                return
            id_prodotto = result[0]
            cursor.execute("""
                           DELETE
                           FROM contiene
                           WHERE id_magazzino = %s
                             AND id_prodotto = %s
                             AND dataScadenza = %s
                           """, (id_magazzino, id_prodotto, data_scadenza))

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Fatto", "Record eliminato con successo.")
            self.carica_tabella()

        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore durante l'eliminazione: {e}")

    def elimina_record_quantita_zero(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="agrilogic"
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contiene WHERE quantita = 0")
        conn.commit()
        cursor.close()
        conn.close()

    def carica_tabella(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="agrilogic"
        )
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT c.id_magazzino,
                              p.nome AS prodotto,
                              c.dataScadenza,
                              c.quantita
                       FROM contiene AS c
                                JOIN prodotto AS p ON c.id_prodotto = p.id
                       """)
        risultati = cursor.fetchall()
        self.tblProdScad.setColumnCount(4)
        self.tblProdScad.setHorizontalHeaderLabels(["Magazzino", "Prodotto", "Scadenza", "Quantità"])
        self.tblProdScad.setRowCount(len(risultati))
        for row_idx, row_data in enumerate(risultati):
            for col_idx, value in enumerate(row_data):
                self.tblProdScad.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        cursor.close()
        conn.close()

    def immagazzina(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="agrilogic"
        )
        cursor = conn.cursor()
        coltura = self.cmbProdImm.currentText()
        cursor.execute("SELECT id FROM prodotto WHERE nome = %s", (coltura,))
        prodotto_row = cursor.fetchone()
        conn.close()

        id_prodotto = prodotto_row[0]
        id_magazzino = int(self.cmbMagazzImm.currentText())
        data_scadenza = self.dateScadenzaImm.date().toPyDate()
        data_immagazzinamento = date.today()
        quantita = self.spinQuantImm.value()
        cursor.execute("""
                       SELECT quantita
                       FROM contiene
                       WHERE id_magazzino = %s
                         AND id_prodotto = %s
                         AND dataScadenza = %s
                       """, (id_magazzino, id_prodotto, data_scadenza))

        existing_row = cursor.fetchone()

        if existing_row:
            nuova_quantita = existing_row[0] + quantita
            cursor.execute("""
                           UPDATE contiene
                           SET quantita = %s
                           WHERE id_magazzino = %s
                             AND id_prodotto = %s
                             AND dataScadenza = %s
                           """, (nuova_quantita, id_magazzino, id_prodotto, data_scadenza))
        else:
            cursor.execute("""
                           INSERT INTO contiene (id_magazzino, id_prodotto, dataImmagazzinazione, dataScadenza,
                                                 quantita)
                           VALUES (%s, %s, %s, %s, %s)
                           """, (id_magazzino, id_prodotto, data_immagazzinamento, data_scadenza, quantita))
        conn.commit()
        cursor.close()
        conn.close()
        self.elimina_record_quantita_zero()
        self.carica_tabella()

    def caricamento_magazzino(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="agrilogic"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM magazzino",)
        result = cursor.fetchall()
        self.cmbMagazzImm.clear()
        ids = [str(row[0]) for row in result]
        self.cmbMagazzImm.addItems(ids)
        cursor.execute("SELECT nome FROM prodotto", )
        result = cursor.fetchall()
        self.cmbProdImm.clear()
        ids = [str(row[0]) for row in result]
        self.cmbProdImm.addItems(ids)
        self.dateScadenzaImm.setDate(date.today())
        conn.close()
        self.elimina_record_quantita_zero()
        self.carica_tabella()

    def modifica_stato_mansione(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="agrilogic"
        )
        cursor = conn.cursor()
        contenuto = self.cmbSelMans.currentText()
        stato = self.cmbStatMans.currentText()
        id = contenuto.split('-')[1].strip()
        cursor.execute("UPDATE Mansione SET stato = %s WHERE id = %s", (stato, id))
        conn.commit()
        cursor.execute(
            "SELECT m.stato FROM user u JOIN assegna a ON u.id = a.id_utente JOIN Mansione m ON a.id_mansione = m.id WHERE u.email =%s",
            (mailUtente,))
        result = cursor.fetchall()
        if result is None or result[0] is None:
            self.cmbStatMans.setEnabled(False)
        else:
            self.cmbStatMans.setEnabled(True)
        cursor.execute(
            "SELECT m.descrizione, m.id FROM `user` u JOIN assegna a ON u.id = a.id_utente JOIN Mansione m ON a.id_mansione = m.id WHERE u.email = %s AND m.stato != 'COMPLETATA'",
            (mailUtente,))
        result = cursor.fetchall()
        if not result:
            self.grbMansioni.hide()
            self.lblNessunaManasione.setText("Nessuna Mansione assegnata")
        else:
            self.cmbSelMans.blockSignals(True)
            self.cmbSelMans.setEnabled(True)
            self.cmbSelMans.clear()
            nomi = [f"{row[0]} - {row[1]}" for row in result]
            self.cmbSelMans.addItems(nomi)
            self.cmbSelMans.blockSignals(False)
            contenuto = self.cmbSelMans.currentText()
            id = contenuto.split('-')[1].strip()
            cursor.execute(
                "SELECT m.stato FROM user u JOIN assegna a ON u.id = a.id_utente JOIN Mansione m ON a.id_mansione = m.id WHERE m.id =%s",
                (id,))
            result = cursor.fetchall()
            if not result:
                self.cmbStatMans.setEnabled(False)
            else:
                self.cmbStatMans.setEnabled(True)
                self.cmbStatMans.clear()
                nomi = [str(row[0]) for row in result]
                self.cmbStatMans.addItems(nomi)
            if self.cmbStatMans.currentText() == "IN_ATTESA":
                self.cmbStatMans.addItems(["IN_CORSO", "COMPLETATA"])
            elif self.cmbStatMans.currentText() == "IN_CORSO":
                self.cmbStatMans.addItems(["COMPLETATA"])

    def modifica_combo_mansioni(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="agrilogic"
        )
        cursor = conn.cursor()
        contenuto = self.cmbSelMans.currentText()
        id = contenuto.split('-')[1].strip()
        cursor.execute(
            "SELECT m.stato FROM user u JOIN assegna a ON u.id = a.id_utente JOIN Mansione m ON a.id_mansione = m.id WHERE m.id =%s",(id,))
        result = cursor.fetchall()
        if not result:
            self.cmbStatMans.setEnabled(False)
        else:
            self.cmbStatMans.setEnabled(True)
            self.cmbStatMans.clear()
            nomi = [str(row[0]) for row in result]
            self.cmbStatMans.addItems(nomi)
        if self.cmbStatMans.currentText() == "IN_ATTESA":
            self.cmbStatMans.addItems(["IN_CORSO", "COMPLETATA"])
        elif self.cmbStatMans.currentText() == "IN_CORSO":
            self.cmbStatMans.addItems(["COMPLETATA"])

    def riempi_combo_mansioni(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="agrilogic"
        )
        cursor = conn.cursor()
        cursor.execute(
            "SELECT m.stato FROM user u JOIN assegna a ON u.id = a.id_utente JOIN Mansione m ON a.id_mansione = m.id WHERE u.email =%s",(mailUtente,))
        result = cursor.fetchall()
        if result is None or result[0] is None:
            self.cmbStatMans.setEnabled(False)
        else:
            self.cmbStatMans.setEnabled(True)
        cursor.execute(
            "SELECT m.descrizione, m.id FROM `user` u JOIN assegna a ON u.id = a.id_utente JOIN Mansione m ON a.id_mansione = m.id WHERE u.email = %s AND m.stato != 'COMPLETATA'",
            (mailUtente,))
        result = cursor.fetchall()
        if not result:
            self.grbMansioni.hide()
            self.lblNessunaManasione.setText("Nessuna Mansione assegnata")
        else:
            self.grbMansioni.show()
            self.lblNessunaManasione.setText("")
            self.cmbSelMans.setEnabled(True)
            self.cmbSelMans.blockSignals(True)
            self.cmbSelMans.clear()
            self.cmbSelMans.blockSignals(False)
            nomi = [f"{row[0]} - {row[1]}" for row in result]
            self.cmbSelMans.addItems(nomi)
        conn.close()

    def raccolta_terreno(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="agrilogic"
        )
        cursor = conn.cursor()
        id_terreno = self.comboTerreni.currentText()
        nome_coltura = self.comboSemina.currentText()
        cursor.execute("SELECT id FROM coltura WHERE nome=%s ", (nome_coltura,))
        result = cursor.fetchone()
        cursor.execute("UPDATE Coltiva SET dataRaccolta = %s WHERE id = ( SELECT id FROM (SELECT MAX(id) AS id FROM Coltiva WHERE id_terreno = %s AND id_coltura = %s) AS sub); ",(date.today(),id_terreno,result[0],))
        conn.commit()
        self.btnRaccolta.setEnabled(False)
        cursor.execute("SELECT dataSeminazione FROM coltiva WHERE id_terreno=%s ORDER BY id DESC LIMIT 1", (id_terreno,))
        result = cursor.fetchone()
        if result is None or result[0] is None:
            self.lblDataSeminazione.setText("Nessuna data di seminazione")
            self.btnSemina.setEnabled(True)
        else:
            self.lblDataSeminazione.setText(result[0].strftime("%Y-%m-%d"))
            self.btnSemina.setEnabled(False)
        cursor.execute(
            "SELECT c.nome FROM coltiva co JOIN coltura c ON co.id_coltura = c.id WHERE co.id_terreno = %s ORDER BY co.id DESC LIMIT 1",
            (id_terreno,))
        result = cursor.fetchone()
        if result is None or result[0] is None:
            self.lblColturaAss.setText("Nessuna coltura assegnata")
        else:
            self.lblColturaAss.setText(result[0])
        cursor.execute("SELECT dataRaccolta FROM coltiva WHERE id_terreno = %s ORDER BY id DESC LIMIT 1",(id_terreno,))
        result = cursor.fetchone()
        if result is None or result[0] is None:
            self.lblDataRaccolta.setText("Nessuna data di raccolta")
            self.btnRaccolta.setEnabled(True)
        else:
            self.lblDataRaccolta.setText(result[0].strftime("%Y-%m-%d"))
            self.btnRaccolta.setEnabled(False)
        conn.close()

    def semina_terreno(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="agrilogic"
        )
        cursor = conn.cursor()
        id_terreno = self.comboTerreni.currentText()
        nome_coltura = self.comboSemina.currentText()
        cursor.execute("SELECT id FROM coltura WHERE nome=%s ", (nome_coltura,))
        result = cursor.fetchone()
        cursor.execute("INSERT INTO coltiva (id_terreno, id_coltura, dataSeminazione) VALUES (%s, %s, %s)",(id_terreno,result[0],date.today()))
        conn.commit()
        cursor.execute("SELECT dataSeminazione FROM coltiva WHERE id_terreno=%s ORDER BY id DESC LIMIT 1", (id_terreno,))
        result = cursor.fetchone()
        if result is None or result[0] is None:
            self.lblDataSeminazione.setText("Nessuna data di seminazione")
            self.btnSemina.setEnabled(True)
        else:
            self.lblDataSeminazione.setText(result[0].strftime("%Y-%m-%d"))
            self.btnSemina.setEnabled(False)
            self.btnSemina.setEnabled(True)
        cursor.execute(
            "SELECT c.nome FROM coltiva co JOIN coltura c ON co.id_coltura = c.id WHERE co.id_terreno = %s ORDER BY co.id DESC LIMIT 1",
            (id_terreno,))
        result = cursor.fetchone()
        if result is None or result[0] is None:
            self.lblColturaAss.setText("Nessuna coltura assegnata")
        else:
            self.lblColturaAss.setText(result[0])
        conn.close()

    def modifica_credenziali(self):
        email = self.txtEmailDipendente.text()
        password = self.txtPasswordDipendente.text()

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="agrilogic"
        )
        cursor = conn.cursor()
        if mailUtente == email:
            cursor.execute("UPDATE user SET password = %s WHERE email = %s", (password, email))
            conn.commit()
            QtWidgets.QMessageBox.warning(self, "Errore", "Password cambiata.")
            self.txtEmailDipendente.setText("")
            self.txtPasswordDipendente.setText("")
        else:
            QtWidgets.QMessageBox.warning(self, "Errore", "Email non valida")

        conn.close()

    def irrigazione_terreni(self):
        seminazione = False
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="agrilogic"
        )
        cursor = conn.cursor()
        id = self.comboTerreni.currentText()
        cursor.execute("SELECT livelloIrrigazione FROM terreno WHERE id = %s", (id,))
        result = cursor.fetchone()
        self.barTerreno.setValue(result[0])
        cursor.execute("SELECT dataSeminazione FROM coltiva WHERE id_terreno=%s ORDER BY id DESC LIMIT 1", (id,))
        result = cursor.fetchone()
        if result is None or result[0] is None:
            self.lblDataSeminazione.setText("Nessuna data di seminazione")
            self.btnSemina.setEnabled(True)
            seminazione = False
        else:
            self.lblDataSeminazione.setText(result[0].strftime("%Y-%m-%d"))
            self.btnSemina.setEnabled(False)
            seminazione = True
        cursor.execute("SELECT dataRaccolta FROM coltiva WHERE id_terreno=%s ORDER BY id DESC LIMIT 1",(id,))
        result = cursor.fetchone()
        if result is None or result[0] is None:
            self.lblDataRaccolta.setText("Nessuna data di raccolta")
            if seminazione is False:
                self.btnRaccolta.setEnabled(False)
            else:
                self.btnRaccolta.setEnabled(True)
        else:
            self.lblDataRaccolta.setText(result[0].strftime("%Y-%m-%d"))
            self.btnRaccolta.setEnabled(False)
        cursor.execute("SELECT c.nome FROM coltiva co JOIN coltura c ON co.id_coltura = c.id WHERE co.id_terreno = %s ORDER BY co.id DESC LIMIT 1", (id,))
        result = cursor.fetchone()
        if result is None or result[0] is None:
            self.lblColturaAss.setText("Nessuna coltura assegnata")
        else:
            self.lblColturaAss.setText(result[0])
        conn.close()

    def irriga_campo(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="agrilogic"
        )
        cursor = conn.cursor()
        livello = 100
        id = self.comboTerreni.currentText()
        cursor.execute("UPDATE terreno SET livelloIrrigazione = %s WHERE id = %s", (livello, id,))
        conn.commit()
        self.barTerreno.setValue(100)
        conn.close()

    def caricamento_terreni(self):
        seminazione = False
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="agrilogic"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT nome FROM coltura")
        result = cursor.fetchall()
        self.comboSemina.blockSignals(True)
        self.comboSemina.clear()
        nomi = [str(row[0]) for row in result]
        self.comboSemina.addItems(nomi)
        self.comboSemina.blockSignals(False)

        cursor.execute("SELECT id FROM terreno")
        result = cursor.fetchall()
        self.comboTerreni.blockSignals(True)
        self.comboTerreni.clear()
        ids = [str(row[0]) for row in result]
        self.comboTerreni.addItems(ids)
        self.comboTerreni.blockSignals(False)
        id = self.comboTerreni.currentText()
        cursor.execute("SELECT dataSeminazione FROM coltiva WHERE id_terreno=%s ORDER BY id DESC LIMIT 1", (id,))
        result = cursor.fetchone()
        if result is None or result[0] is None:
            self.lblDataSeminazione.setText("Nessuna data di seminazione")
            self.btnSemina.setEnabled(True)
            seminazione = False
        else:
            self.lblDataSeminazione.setText(result[0].strftime("%Y-%m-%d"))
            self.btnSemina.setEnabled(False)
            seminazione = True
        cursor.execute("SELECT dataRaccolta FROM coltiva WHERE id_terreno = %s ORDER BY id DESC LIMIT 1",(id,))
        result = cursor.fetchone()
        if result is None or result[0] is None:
            self.lblDataRaccolta.setText("Nessuna data di raccolta")
            if seminazione is False:
                self.btnRaccolta.setEnabled(True)
            else:
                self.btnRaccolta.setEnabled(False)
        else:
            self.lblDataRaccolta.setText(result[0].strftime("%Y-%m-%d"))
            self.btnRaccolta.setEnabled(False)
        cursor.execute("SELECT c.nome FROM coltiva co JOIN coltura c ON co.id_coltura = c.id WHERE co.id_terreno = %s ORDER BY co.id DESC LIMIT 1", (id,))
        result = cursor.fetchone()
        if result is None or result[0] is None:
            self.lblColturaAss.setText("Nessuna coltura assegnata")
        else:
            self.lblColturaAss.setText(result[0])
        conn.close()

class LoginWindow(QtWidgets.QMainWindow, Ui_login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnLogin.clicked.connect(self.login_logic)
        self.btnRecuperaPassword.clicked.connect(self.recuperaPassword)

    def login_logic(self):
        email = self.txtEmail.text()
        password = self.txtPassword.text()
        global mailUtente

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="agrilogic"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT ruolo FROM user WHERE email = %s AND password = %s", (email, password))
        result = cursor.fetchone()

        if result is None:
            QtWidgets.QMessageBox.warning(self, "Errore", "Credenziali non valide.")
        elif result[0]=="dipendente":
            mailUtente = email
            self.main = MainWindow()
            self.main.caricamento_magazzino()
            self.main.show()
            self.close()
        elif result[0]=="amministratore":
            mailUtente = email
            self.main = AdminWindow()
            self.main.caricaUtenti()
            self.main.show()
            self.close()

        conn.close()

    def recuperaPassword(self):
        self.main = recuperaPassword()
        self.main.show()
        self.close()

class recuperaPassword(QtWidgets.QMainWindow, Ui_recuperapassword):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnCambiaPassword.clicked.connect(self.cambia_password)
        self.btnAnnulla.clicked.connect(self.annulla)

    def annulla(self):
        self.main = LoginWindow()
        self.main.show()
        self.close()

    def cambia_password(self):
        email = self.txtNuovaEmail.text()
        password = self.txtNuovaPassword.text()

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="agrilogic"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result:
            cursor.execute("UPDATE user SET password = %s WHERE email = %s", (password, email))
            conn.commit()
            self.main = LoginWindow()
            self.main.show()
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Errore", "Email non valida.")

        conn.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())

