# Team Statistics Feature

## Panoramica

La pagina "Statistics" consente di visualizzare l'andamento delle flag rubate per ogni team in due modalità:
1. **Overall Statistics**: Statistiche generali che considerano tutti i tick, con ordinamento basato sulla scoreboard
2. **By Tick**: Statistiche specifiche per un singolo tick selezionabile

## 🚨 **NUOVO: Sistema di Alert per Exploit**

Il sistema ora include un avanzato sistema di notifiche che avvisa automaticamente quando si smette di exploitare un team (passaggio da 1+ flag a 0 flag tra tick consecutivi).

### Funzionalità degli Alert

- **🔔 Rilevamento Automatico**: Controlla automaticamente i cambiamenti tra tick consecutivi
- **📱 Notifiche Multiple**: Popup dettagliati + toast notifications + badge fluttuante
- **🎵 Audio Alert**: Suono di notifica opzionale (configurabile)
- **⚙️ Impostazioni Personalizzabili**: Controllo completo su tipologie di notifiche
- **📋 Storico**: Mantiene uno storico delle notifiche recenti

### Tipi di Notifiche

1. **Popup Dialog**: 
   - Mostra dettagli completi degli exploit interrotti
   - Lista di team e servizi interessati
   - Confronto tra tick precedente e corrente

2. **Toast Notifications**:
   - Notifiche discrete nell'angolo dello schermo
   - Azione rapida per visualizzare dettagli
   - Auto-dismiss dopo 5 secondi

3. **Badge Fluttuante**:
   - Indicatore visibile del numero di alert attivi
   - Sempre visibile fino al dismiss
   - Click per riaprire l'ultimo popup

4. **Audio Alert**:
   - Suono di notifica personalizzabile
   - Tono a 800Hz per 0.5 secondi
   - Disabilitabile nelle impostazioni

## Modalità di Visualizzazione

### 1. Overall Statistics (Modalità Predefinita)
- **Statistiche Globali**: Mostra il totale delle flag rubate da ogni team durante tutta la CTF
- **Ordinamento Scoreboard**: I team sono ordinati secondo la classifica ufficiale da `http://10.10.0.1/api/scoreboard`
- **Evidenziazione Posizioni**: 
  - 🥇 1° posto: sfondo dorato
  - 🥈 2° posto: sfondo argento  
  - 🥉 3° posto: sfondo bronzo
- **Totale Generale**: Mostra il numero totale di flag rubate nella CTF

### 2. By Tick (Modalità Dettagliata)
- **Statistiche per Tick**: Mostra le flag rubate nel tick specificato
- **🆕 Ultimo Tick Automatico**: All'apertura, mostra automaticamente l'ultimo tick disponibile
- **🆕 Auto Refresh Sincronizzato**: Aggiornamento automatico sincronizzato con i tick reali (ogni 2 minuti)
- **Navigazione Tick**: Controlli per spostarsi tra i tick o saltare a uno specifico
- **🆕 Pulsante "Latest"**: Salta rapidamente all'ultimo tick disponibile  
- **Informazioni Temporali**: Visualizza orari di inizio e fine del tick selezionato
- **🆕 Check Manual**: Pulsante per controllare manualmente gli alert

## Funzionalità Comuni

### Visualizzazione Matrice
- **Righe**: Team (ordinati per scoreboard nella modalità overall, alfabeticamente nella modalità tick)
- **Colonne**: Servizi (sploit) + colonna totale
- **Celle Rosse**: Flag rubate = 0 (con animazione pulsante per attirare l'attenzione)
- **Colonna Verde**: Totali per team sulla destra

### Controlli Interfaccia
- **Toggle Modalità**: Interruttore per passare tra "Overall Stats" e "By Tick"
- **Refresh**: Pulsante per aggiornare manualmente i dati
- **Auto Refresh**: Solo disponibile in modalità tick, attiva anche gli alert automatici
- **🆕 Impostazioni Notifiche**: Configurazione completa del sistema di alert

## API Endpoints

### `/api/team_stats_compare`

**Metodo**: GET

**Parametri**:
- `current_tick` (opzionale): Tick corrente da analizzare
- `previous_tick` (opzionale): Tick precedente per il confronto

**Descrizione**: Confronta le statistiche tra due tick e rileva exploit interrotti

**Risposta**:
```json
{
  "current_tick": 15,
  "previous_tick": 14,
  "total_alerts": 2,
  "alerts": [
    {
      "team": "10.60.1.1",
      "service": "WebService",
      "previous_flags": 3,
      "current_flags": 0,
      "type": "exploit_stopped"
    },
    {
      "team": "10.60.2.1",
      "service": "Database",
      "previous_flags": 1,
      "current_flags": 0,
      "type": "exploit_stopped"
    }
  ]
}
```

### `/api/team_stats_overall`

**Metodo**: GET

**Descrizione**: Restituisce le statistiche generali per tutti i tick

**Risposta**:
```json
{
  "teams": ["team1", "team2", "team3"],  // Ordinati per scoreboard
  "services": ["service1", "service2", "service3"],
  "stats_matrix": {
    "team1": {
      "service1": 25,
      "service2": 3,
      "service3": 15
    },
    "team2": {
      "service1": 18,
      "service2": 7,
      "service3": 0
    }
  },
  "team_totals": {
    "team1": 43,
    "team2": 25
  },
  "total_flags": 68
}
```

### `/api/team_stats`

**Metodo**: GET

**Parametri**:
- `tick` (opzionale): Numero del tick da visualizzare

**Descrizione**: Restituisce le statistiche per un tick specifico

**Risposta**:
```json
{
  "tick": 5,
  "tick_duration": 60,
  "teams": ["team1", "team2", "team3"],
  "services": ["service1", "service2", "service3"],
  "stats_matrix": {
    "team1": {
      "service1": 3,
      "service2": 0,
      "service3": 5
    }
  },
  "team_totals": {
    "team1": 8
  },
  "start_time": 1640995200,
  "tick_start_time": 1640995440,
  "tick_end_time": 1640995500
}
```

## Utilizzo

### Modalità Overall
1. Aprire la pagina "Statistics" (modalità predefinita)
2. Visualizzare la classifica generale ordinata per scoreboard
3. Identificare team con prestazioni migliori/peggiori
4. Le celle rosse mostrano servizi problematici per ogni team

### Modalità By Tick con Alert
1. Fare clic su "By Tick" nel toggle in alto
2. **La pagina si apre automaticamente sull'ultimo tick disponibile**
3. **L'Auto Refresh si attiva automaticamente e si sincronizza con i tick reali (ogni 2 minuti)**
4. Utilizzare i controlli per navigare tra i tick:
   - Pulsanti "Previous/Next" per navigazione sequenziale
   - Input diretto del numero tick
   - **🆕 Pulsante "Latest"** per saltare all'ultimo tick
5. Gli alert appariranno automaticamente quando un exploit smette di funzionare
6. Configurare le notifiche tramite l'icona delle impostazioni

### Gestione Alert
1. **Alert Automatici**: Si attivano con auto refresh in modalità tick
2. **Controllo Manuale**: Usare il pulsante "Check" per verifiche manuali
3. **Configurazione**: Cliccare sull'icona impostazioni per personalizzare notifiche
4. **Storico**: Visualizzare le notifiche recenti nelle impostazioni

## Configurazione Alert

Le impostazioni degli alert includono:

- **✅ Abilita Alert**: Master switch per tutto il sistema
- **🍞 Toast Notifications**: Notifiche discrete nell'angolo
- **📱 Popup Dialogs**: Dialog dettagliati con informazioni complete
- **🔊 Suoni di Notifica**: Audio alert configurabile
- **📚 Storico**: Visualizzazione e pulizia delle notifiche recenti

Le impostazioni vengono salvate automaticamente nel browser.

## Integrazione con Scoreboard

La modalità "Overall Statistics" si integra con la scoreboard ufficiale:
- **URL Scoreboard**: `http://10.10.0.1/api/scoreboard`
- **Ordinamento Automatico**: I team vengono ordinati automaticamente per punteggio
- **Fallback**: In caso di errore, viene utilizzato l'ordinamento alfabetico
- **Timeout**: 5 secondi per la richiesta alla scoreboard

## Note Tecniche

- I dati sono filtrati per mostrare solo le flag con status "ACCEPTED"
- Gli alert rilevano solo transizioni da >0 a 0 flag (exploit interrotti)
- L'ordinamento per scoreboard viene aggiornato ad ogni richiesta alla modalità overall
- Le due modalità sono indipendenti e mantengono stati separati
- L'auto refresh attiva automaticamente il controllo degli alert
- **🆕 Auto refresh sincronizzato**: In modalità tick, l'aggiornamento è sincronizzato con i tick reali (ogni 2 minuti)
- **🆕 Caricamento ultimo tick**: La modalità tick si apre sempre sull'ultimo tick disponibile
- Il sistema di notifiche è completamente asincrono e non blocca l'interfaccia
- Le impostazioni vengono persistite nel localStorage del browser

## Legenda Colori

- 🔴 **Rosso**: Nessuna flag rubata (0) - potenziali problemi
- 🟢 **Verde**: Colonna totali
- 🟡 **Giallo**: 1° posto in classifica (solo modalità overall)
- ⚪ **Grigio**: 2° posto in classifica (solo modalità overall)  
- 🟠 **Arancione**: 3° posto in classifica (solo modalità overall)
- ⚠️ **Alert**: Notifiche automatiche per exploit interrotti

## 🧪 Guida al Testing

### Prerequisiti per il Testing

1. **Ambiente Attivo**: Assicurarsi che l'ambiente S4DFarm sia avviato:
   ```bash
   cd /home/cavallo/Desktop/CyberSecurity/Destructive/S4DFarm
   ./start_farm.sh
   ```

2. **Database Popolato**: Verificare che ci siano dati di flag nel database:
   - Controllare che ci siano flag con status "ACCEPTED"
   - Verificare che ci siano almeno 2-3 tick di dati

3. **Scoreboard Attiva**: Verificare che la scoreboard sia raggiungibile:
   ```bash
   curl http://10.10.0.1/api/scoreboard
   ```

### Testing Step-by-Step

#### 1. Test delle API Endpoints

**Testare Team Stats Overall:**
```bash
# Verificare l'endpoint delle statistiche generali
curl -X GET "http://localhost:5000/api/team_stats_overall" | jq .

# Risposta attesa:
# - Lista di team ordinati per scoreboard
# - Matrice delle statistiche con totali
# - Numero totale di flag
```

**Testare Team Stats per Tick Specifico:**
```bash
# Testare con tick specifico
curl -X GET "http://localhost:5000/api/team_stats?tick=5" | jq .

# Testare senza parametri (tick corrente)
curl -X GET "http://localhost:5000/api/team_stats" | jq .
```

**Testare Confronto Tick (Alert System):**
```bash
# Confrontare due tick consecutivi
curl -X GET "http://localhost:5000/api/team_stats_compare?current_tick=10&previous_tick=9" | jq .

# Auto-detect tick precedente
curl -X GET "http://localhost:5000/api/team_stats_compare?current_tick=10" | jq .
```

#### 2. Test dell'Interfaccia Web

**Accesso alla Pagina:**
1. Aprire il browser e navigare a: `http://localhost:3000` (o porta configurata)
2. Fare login con le credenziali admin
3. Navigare alla sezione "Statistics"

**Test Modalità Overall:**
1. Verificare che la modalità "Overall Stats" sia selezionata di default
2. Controllare che i team siano ordinati per punteggio (primi 3 evidenziati)
3. Verificare che le celle con 0 flag siano rosse e pulsanti
4. Controllare che la colonna totali sia verde
5. Verificare il totale generale in fondo alla tabella

**Test Modalità By Tick:**
1. Cliccare su "By Tick" nel toggle
2. Verificare che appaia il selettore del tick
3. Testare la navigazione: 
   - Pulsanti "Previous/Next"
   - Input diretto del numero tick
   - Pulsante "Latest" per l'ultimo tick
4. Verificare che appaiano le informazioni temporali del tick
5. Controllare che l'ordinamento sia alfabetico

#### 3. Test del Sistema di Alert

**Preparazione Dati per Alert:**

Per testare gli alert, devi simulare una situazione dove un exploit smette di funzionare. Puoi farlo in due modi:

**Metodo 1 - Simulazione Database (Raccomandato):**
```python
# Script Python per simulare dati di test
# Salva come test_alerts.py
import sqlite3
import time

def simulate_exploit_stop():
    # Connetti al database S4DFarm
    conn = sqlite3.connect('path/to/your/database.db')
    cursor = conn.cursor()
    
    # Trova l'ultimo tick
    cursor.execute("SELECT MAX(tick) FROM flags WHERE status='ACCEPTED'")
    last_tick = cursor.fetchone()[0] or 0
    
    current_tick = last_tick + 1
    
    # Inserisci flag per il tick precedente (simula exploit funzionante)
    cursor.execute("""
        INSERT INTO flags (team, service, flag, status, tick, timestamp)
        VALUES (?, ?, ?, 'ACCEPTED', ?, ?)
    """, ("10.60.1.1", "TestService", "flag123", last_tick, int(time.time())))
    
    # Non inserire flag per il tick corrente (simula exploit interrotto)
    # Questo creerà un alert quando confrontato
    
    conn.commit()
    conn.close()
    print(f"Dati di test inseriti. Tick precedente: {last_tick}, Tick corrente: {current_tick}")

if __name__ == "__main__":
    simulate_exploit_stop()
```

**Metodo 2 - Test Client:**
```python
# Script per testare submission di flag
# Usa il client esistente modificato
import time
import requests

def submit_test_flags():
    # Simula submission normale
    response1 = requests.post('http://localhost:5000/api/flags', {
        'team': '10.60.1.1',
        'service': 'TestService', 
        'flag': 'TEST_FLAG_WORKING'
    })
    
    # Aspetta un tick
    time.sleep(60)  # Assumendo tick da 60 secondi
    
    # Non inviare flag per il tick successivo
    # Questo simula un exploit che smette di funzionare
    print("Flag inviata per tick precedente, nessuna flag per tick corrente")

submit_test_flags()
```

**Test degli Alert nell'UI:**

1. **Attivare Auto Refresh:**
   - Andare in modalità "By Tick"
   - Attivare l'interruttore "Auto Refresh"
   - Verificare che si aggiorni ogni 30 secondi

2. **Test Alert Automatici:**
   - Con auto refresh attivo, aspettare che si verifichi un cambio tick
   - Se ci sono exploit interrotti, dovrebbero apparire automaticamente:
     - Popup con dettagli completi
     - Toast notification nell'angolo
     - Badge fluttuante con numero alert

3. **Test Alert Manuali:**
   - Cliccare il pulsante "Check" per controllo manuale
   - Verificare che gli alert appaiano anche senza auto refresh

4. **Test Configurazioni Alert:**
   - Cliccare l'icona impostazioni (⚙️)
   - Testare ogni tipo di notifica:
     - ☑️ Disattivare popup → verificare che non appaiano
     - ☑️ Disattivare toast → verificare che non appaiano  
     - ☑️ Disattivare audio → verificare che non suoni
   - Testare il pulsante "Test Audio"
   - Verificare lo storico delle notifiche

#### 4. Test della Scoreboard Integration

**Test Ordinamento:**
```bash
# Verificare che la scoreboard sia raggiungibile
curl http://10.10.0.1/api/scoreboard

# Verificare che l'ordinamento in "Overall Stats" rispetti la scoreboard
# I primi 3 team dovrebbero essere evidenziati con colori oro/argento/bronzo
```

**Test Fallback:**
```bash
# Simulare scoreboard non raggiungibile (temporaneamente)
# Bloccare il traffico verso 10.10.0.1 e verificare che:
# 1. L'ordinamento fallback sia alfabetico
# 2. Non ci siano errori nell'UI
# 3. Appaia un messaggio di fallback
```

#### 5. Test di Performance e Stress

**Test con Molti Dati:**
```python
# Script per generare molti dati di test
import sqlite3
import random
import time

def generate_large_dataset():
    conn = sqlite3.connect('path/to/database.db')
    cursor = conn.cursor()
    
    teams = [f"10.60.{i}.1" for i in range(1, 21)]  # 20 team
    services = [f"Service{i}" for i in range(1, 11)]  # 10 servizi
    
    for tick in range(1, 101):  # 100 tick
        for team in teams:
            for service in services:
                # Simula successo casuale degli exploit
                if random.random() > 0.3:  # 70% successo
                    flags_count = random.randint(1, 5)
                    for _ in range(flags_count):
                        cursor.execute("""
                            INSERT INTO flags (team, service, flag, status, tick, timestamp)
                            VALUES (?, ?, ?, 'ACCEPTED', ?, ?)
                        """, (team, service, f"flag_{tick}_{team}_{service}_{_}", 
                             tick, int(time.time()) + tick * 60))
    
    conn.commit()
    conn.close()
    print("Dataset di test generato: 20 team, 10 servizi, 100 tick")

generate_large_dataset()
```

**Test Responsività:**
1. Caricare la pagina con il dataset grande
2. Verificare tempi di caricamento < 3 secondi
3. Testare scroll e interazioni fluide
4. Verificare che l'auto refresh non rallenti l'UI

#### 6. Test di Integrazione Completa

**Scenario Realistico:**
1. **Preparazione:**
   - Avviare l'ambiente completo
   - Avere almeno 3-4 team attivi
   - Configurare 2-3 servizi

2. **Simulazione CTF:**
   ```bash
   # Avviare client automatici per simulare exploit
   cd client/
   python start_sploit.py --teams 3 --services 2 --duration 300
   ```

3. **Monitoraggio Real-time:**
   - Aprire la pagina Statistics
   - Attivare modalità "By Tick" con auto refresh
   - Configurare tutti i tipi di alert
   - Osservare l'evoluzione in tempo reale

4. **Test Scenario Critico:**
   - Fermare intenzionalmente alcuni exploit
   - Verificare che gli alert si attivino correttamente
   - Controllare che le informazioni siano accurate

### Troubleshooting Common Issues

**Problema: Nessun Dato Visualizzato**
```bash
# Verificare connessione database
sqlite3 path/to/database.db "SELECT COUNT(*) FROM flags WHERE status='ACCEPTED';"

# Verificare configurazione API
curl -v http://localhost:5000/api/team_stats
```

**Problema: Alert Non Funzionano**
1. Verificare che ci siano almeno 2 tick di dati
2. Controllare console browser per errori JavaScript
3. Verificare che auto refresh sia attivo
4. Testare manualmente con pulsante "Check"

**Problema: Scoreboard Non Si Carica**
```bash
# Testare connettività
ping 10.10.0.1
curl -v http://10.10.0.1/api/scoreboard
```

**Problema: Performance Lente**
1. Verificare dimensione database
2. Controllare indici su tabella flags:
   ```sql
   CREATE INDEX idx_flags_tick_status ON flags(tick, status);
   CREATE INDEX idx_flags_team_service ON flags(team, service);
   ```

### Validazione Finale

Per confermare che tutto funzioni correttamente:

1. ✅ **API Endpoints**: Tutte le chiamate curl restituiscono dati validi
2. ✅ **UI Base**: Entrambe le modalità mostrano dati correttamente
3. ✅ **Ordinamento**: Overall stats rispetta la scoreboard
4. ✅ **Alert System**: Notifiche appaiono per exploit interrotti
5. ✅ **Configurazioni**: Impostazioni alert funzionano
6. ✅ **Performance**: Caricamento < 3 secondi con dati realistici
7. ✅ **Real-time**: Auto refresh aggiorna correttamente

### Script di Test Automatico

```bash
#!/bin/bash
# test_statistics.sh - Script di test automatico

echo "🧪 Avvio test completo Statistics..."

# Test API
echo "📡 Testing API endpoints..."
curl -f http://localhost:5000/api/team_stats_overall > /dev/null && echo "✅ Overall stats OK" || echo "❌ Overall stats FAIL"
curl -f http://localhost:5000/api/team_stats > /dev/null && echo "✅ Tick stats OK" || echo "❌ Tick stats FAIL"
curl -f http://localhost:5000/api/team_stats_compare > /dev/null && echo "✅ Compare stats OK" || echo "❌ Compare stats FAIL"

# Test Scoreboard
echo "🏆 Testing scoreboard integration..."
curl -f http://10.10.0.1/api/scoreboard > /dev/null && echo "✅ Scoreboard OK" || echo "⚠️ Scoreboard not reachable (fallback mode)"

# Test Database
echo "🗄️ Testing database..."
if command -v sqlite3 &> /dev/null; then
    count=$(sqlite3 database.db "SELECT COUNT(*) FROM flags WHERE status='ACCEPTED';" 2>/dev/null || echo "0")
    echo "📊 Found $count accepted flags in database"
else
    echo "⚠️ sqlite3 not available, skipping database check"
fi

echo "✨ Test completato! Aprire http://localhost:3000 per test manuale UI"
```

Salva questo script e rendilo eseguibile:
```bash
chmod +x test_statistics.sh
./test_statistics.sh
```
