import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.opzione_selected = None
        self._teamSelected = None

    def fillDD(self):
        elementi = self._model.get_year()  # Recupera lista di elementi

        # Converte ciascun anno in una Option (occhio: map() da un iteratore, meglio usare list)
        listOfOptions = [
            ft.dropdown.Option(text=el, data=el)
            for el in elementi
        ]

        self._view._ddAnno.options = listOfOptions  # Assegna le opzioni al dropdown
        self._view._ddAnno.on_change = self.readDDValue  # Imposta il metodo da chiamare al cambio selezione
        self._view.update_page()

    def readDDValue(self, e):
        selected = e.control.value  # Prende il valore selezionato dal dropdown (es. "2003")
        try:
            self.opzione_selected = int(selected)
            print(f"Hai selezionato l'anno: {selected}")
        except:
            self._view.controls.clear()
            self._view._txtOutSquadre.controls.append(ft.Text("errore", color="blue"))
            self._view.update_page()

        lista_squadre = self._model.get_squadre(self.opzione_selected)
        self._view._txtOutSquadre.controls.append(
            ft.Text(f"Numero di squadre che hanno giocato quell'anno: {len(lista_squadre)}", color="blue")
        )
        self._view._txtOutSquadre.controls.append(
            ft.Text(f"Elenco squadre: {', '.join(lista_squadre)}", color="blue")
        )
        self._view.update_page()


    def handleCreaGrafo(self, e):
        if self.opzione_selected is None:
            self._view.controls.clear()
            self._view._txtOutSquadre.controls.append(ft.Text("errore", color="blue"))
            self._view.update_page()
        else:
            self._model.build_graph(self.opzione_selected)
            n, a = self._model.getGraphDetails()
            self._view.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"i nodi sono: {n} e gli archi sono {a}", color="blue"))
            self._view.update_page()
            self.fillDD2()

    def fillDD2(self):
        """Popola il dropdown con le squadre disponibili."""
        squadre = self._model.get_s()

        # Crea le opzioni del dropdown: text=nome, data=ID
        self._view._ddSquadra.options = [
            ft.dropdown.Option(text= s.name, data=s)
            for s in squadre
        ]

        # Configura il callback per la selezione
        self._view._ddSquadra.on_change = self.readDD2
        self._view.update_page()

    def readDD2(self, e):
        """Gestisce la selezione di una squadra dal dropdown."""
        if not e.control.value:
            return

        selected_name = e.control.value
        selected_team_object = None

        # Cerca l'oggetto squadra selezionato
        for option in e.control.options:
            if option.text == selected_name:
                selected_team_object = option.data
                break

        if selected_team_object is not None:
            self._teamSelected = selected_team_object  # Salva l'oggetto squadra completo
            print(f"Squadra selezionata: {selected_team_object.name}")
        else:
            print(f"Errore: squadra '{selected_name}' non trovata")

    def handleDettagli(self, e):
        if self._teamSelected is None:
            self._view._txt_result.controls.clear()  # Pulisci solo il contenuto di _txtOutSquadre
            self._view._txt_result.controls.append(ft.Text("Errore: nessuna squadra selezionata", color="blue"))
        else:
            details2 = self._model.get_details2(self._teamSelected.ID)
            print(f"Dettagli squadra: {details2}")  # Debug in console

            # Pulisci solo il contenuto di _txtOutSquadre e aggiungi il nuovo testo
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text(f"Dettagli squadra: {'\n '.join(str(d) for d in details2)}")
            )

        self._view.update_page()  # Aggiorna la view una sola volta

    def handlePercorso(self, e):
        pass






