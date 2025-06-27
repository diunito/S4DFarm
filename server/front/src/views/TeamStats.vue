<template>
  <q-page class="q-pa-md">
    <!-- Componente per gli alert di exploit -->
    <exploit-alerts 
      :current-tick="currentTick"
      :auto-check="viewMode === 'tick' && autoRefresh"
      @alert-triggered="onAlertTriggered"
      ref="exploitAlerts"
    />

    <div class="q-mb-md">
      <h4 class="q-my-md">Team Statistics</h4>
      
      <!-- Selector per modalità -->
      <div class="q-mb-md">
        <q-btn-toggle
          v-model="viewMode"
          @update:model-value="onViewModeChange"
          toggle-color="primary"
          :options="[
            {label: 'Overall Stats', value: 'overall'},
            {label: 'By Tick', value: 'tick'}
          ]"
        />
      </div>
      
      <!-- Modalità Overall -->
      <div v-if="viewMode === 'overall'" class="q-mb-md">
        <q-card flat bordered class="q-pa-md bg-blue-1">
          <div class="row q-gutter-md">
            <div class="col">
              <div class="text-caption">Mode</div>
              <div class="text-h6">Overall Statistics</div>
            </div>
            <div class="col" v-if="overallStats">
              <div class="text-caption">Total Flags Stolen</div>
              <div class="text-h6">{{ overallStats.total_flags }}</div>
            </div>
            <div class="col">
              <div class="text-caption">Ordering</div>
              <div class="text-body2">Based on Scoreboard</div>
            </div>
          </div>
        </q-card>
      </div>
      
      <!-- Modalità Tick -->
      <div v-if="viewMode === 'tick'">
        <!-- Info sul tick corrente -->
        <div v-if="tickStats" class="q-mb-md">
          <q-card flat bordered class="q-pa-md bg-blue-1">
            <div class="row q-gutter-md">
              <div class="col">
                <div class="text-caption">Tick Duration</div>
                <div class="text-h6">{{ tickStats.tick_duration }}s</div>
              </div>
              <div class="col">
                <div class="text-caption">Tick Start</div>
                <div class="text-body2">{{ formatTime(tickStats.tick_start_time) }}</div>
              </div>
              <div class="col">
                <div class="text-caption">Tick End</div>
                <div class="text-body2">{{ formatTime(tickStats.tick_end_time) }}</div>
              </div>
              <div v-if="autoRefresh" class="col">
                <div class="text-caption">Auto Refresh</div>
                <div class="text-body2 text-positive">
                  <q-icon name="sync" class="q-mr-xs" />
                  Sincronizzato ({{ tickStats.tick_duration }}s)
                </div>
              </div>
              <div class="col">
                <div class="text-caption">Exploit Alerts</div>
                <q-btn 
                  size="sm" 
                  color="secondary" 
                  icon="search" 
                  @click="checkExploitAlerts"
                  :loading="checkingAlerts"
                >
                  Check
                  <q-tooltip>Check for exploit alerts between previous and current tick</q-tooltip>
                </q-btn>
              </div>
            </div>
          </q-card>
        </div>
        
        <!-- Controlli per navigare tra i tick -->
        <div class="row q-mb-md q-gutter-md items-center">
          <q-btn 
            @click="changeTick(-1)" 
            icon="chevron_left" 
            :disable="currentTick <= 1"
            color="primary"
            round
            size="sm"
          />
          <q-input
            v-model.number="currentTick"
            @update:model-value="(value) => loadTickStats(value)"
            type="number"
            min="1"
            dense
            style="width: 100px"
            label="Tick"
          />
          <q-btn 
            @click="changeTick(1)" 
            icon="chevron_right" 
            color="primary"
            round
            size="sm"
          />
          <q-btn 
            @click="jumpToLatestTick" 
            icon="skip_next" 
            color="info"
            round
            size="sm"
            title="Vai all'ultimo tick"
          />
          <q-btn 
            @click="loadTickStats(currentTick)" 
            icon="refresh" 
            color="secondary"
            round
            size="sm"
          />
          <q-space />
          <notification-settings />
          <q-btn 
            @click="autoRefresh = !autoRefresh" 
            :icon="autoRefresh ? 'pause' : 'play_arrow'"
            :color="autoRefresh ? 'negative' : 'positive'"
            round
            size="sm"
            class="q-ml-sm"
          >
            <q-tooltip>{{ autoRefresh ? 'Stop Auto Refresh' : 'Start Auto Refresh' }}</q-tooltip>
          </q-btn>
        </div>
      </div>
    </div>

    <!-- Tabella delle statistiche -->
    <div v-if="loading" class="text-center q-pa-lg">
      <q-spinner size="50px" color="primary" />
    </div>

    <div v-else-if="currentStats" class="stats-table-container">
      <q-table
        :rows="tableRows"
        :columns="columns"
        row-key="team"
        flat
        bordered
        dense
        class="stats-table"
      >
        <!-- Header personalizzato per evidenziare le colonne dei servizi -->
        <template v-slot:header="props">
          <q-tr :props="props">
            <q-th
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
              :class="getHeaderClass(col.name)"
            >
              {{ col.label }}
            </q-th>
          </q-tr>
        </template>

        <!-- Body personalizzato per evidenziare le celle con 0 flag -->
        <template v-slot:body="props">
          <q-tr :props="props" :class="getRowClass(props.rowIndex)">
            <q-td
              v-for="col in props.cols"
              :key="col.name"
              :props="props"
              :class="getCellClass(col.name, col.value)"
            >
              <span v-if="col.name !== 'team' && col.value === 0" class="zero-flags">
                {{ col.value }}
              </span>
              <span v-else>{{ col.value }}</span>
            </q-td>
          </q-tr>
        </template>
      </q-table>
      
      <!-- Legenda -->
      <div class="q-mt-md">
        <q-card flat bordered class="q-pa-md">
          <div class="text-h6 q-mb-sm">Legend</div>
          <div class="row q-gutter-md">
            <div class="flex items-center">
              <div class="legend-box bg-red-2"></div>
              <span class="q-ml-sm">No flags stolen (0)</span>
            </div>
            <div class="flex items-center">
              <div class="legend-box bg-green-1"></div>
              <span class="q-ml-sm">Total flags</span>
            </div>
            <div v-if="viewMode === 'overall'" class="flex items-center">
              <div class="legend-box bg-yellow-1"></div>
              <span class="q-ml-sm">Teams ranked by scoreboard</span>
            </div>
            <div v-if="viewMode === 'tick'" class="flex items-center">
              <q-icon name="warning" color="negative" />
              <span class="q-ml-sm">Auto-alerts when exploit stops working</span>
            </div>
          </div>
        </q-card>
      </div>
    </div>

    <div v-else class="text-center q-pa-lg">
      <q-banner class="bg-negative text-white">
        Errore nel caricamento delle statistiche
      </q-banner>
    </div>
  </q-page>
</template>

<script>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import api from '@/services/api'
import ExploitAlerts from '@/components/ExploitAlerts.vue'
import NotificationSettings from '@/components/NotificationSettings.vue'
import { useExploitNotifications } from '@/composables/useExploitNotifications'

export default {
  name: 'TeamStats',
  components: {
    ExploitAlerts,
    NotificationSettings
  },
  setup() {
    const viewMode = ref('overall') // 'overall' o 'tick'
    const overallStats = ref(null)
    const tickStats = ref(null)
    const loading = ref(false)
    const currentTick = ref(1)
    const autoRefresh = ref(false)
    const checkingAlerts = ref(false)
    const exploitAlerts = ref(null)
    let refreshInterval = null
    let previousTickValue = null

    // Usa il composable per le notifiche
    const { manualCheck } = useExploitNotifications()

    const currentStats = computed(() => {
      return viewMode.value === 'overall' ? overallStats.value : tickStats.value
    })

    const columns = computed(() => {
      if (!currentStats.value) return []
      
      const cols = [
        {
          name: 'team',
          label: 'Team',
          field: 'team',
          align: 'left',
          sortable: false // Disabilitato perché usiamo l'ordine della scoreboard
        }
      ]

      // Aggiungi colonne per ogni servizio
      currentStats.value.services.forEach(service => {
        cols.push({
          name: service,
          label: service,
          field: service,
          align: 'center',
          sortable: true
        })
      })

      // Aggiungi colonna totale
      cols.push({
        name: 'total',
        label: 'Total',
        field: 'total',
        align: 'center',
        sortable: true
      })

      return cols
    })

    const tableRows = computed(() => {
      if (!currentStats.value) return []

      return currentStats.value.teams.map((team, index) => {
        const row = { team, originalIndex: index }
        
        // Aggiungi i dati per ogni servizio
        currentStats.value.services.forEach(service => {
          row[service] = currentStats.value.stats_matrix[team][service] || 0
        })
        
        // Aggiungi il totale
        row.total = currentStats.value.team_totals[team] || 0
        
        return row
      })
    })

    const loadOverallStats = async () => {
      loading.value = true
      try {
        const response = await api.get('/team_stats_overall')
        overallStats.value = response.data
      } catch (error) {
        console.error('Errore nel caricamento delle statistiche generali:', error)
        overallStats.value = null
      } finally {
        loading.value = false
      }
    }

    const loadTickStats = async (requestedTick = null) => {
      loading.value = true
      try {
        const params = {}
        if (requestedTick !== null) {
          params.tick = requestedTick
        }
        // Se non specifichiamo il tick, l'API restituirà l'ultimo tick disponibile
        
        const response = await api.get('/team_stats', { params })
        tickStats.value = response.data
        
        // Aggiorna currentTick con quello effettivo restituito dall'API
        if (currentTick.value !== response.data.tick) {
          previousTickValue = currentTick.value
          currentTick.value = response.data.tick
        }
      } catch (error) {
        console.error('Errore nel caricamento delle statistiche del tick:', error)
        tickStats.value = null
      } finally {
        loading.value = false
      }
    }

    const onViewModeChange = () => {
      stopAutoRefresh() // Stop auto refresh quando si cambia modalità
      
      if (viewMode.value === 'overall') {
        autoRefresh.value = false
        loadOverallStats()
      } else {
        // In modalità tick, carica l'ultimo tick disponibile e attiva auto refresh
        loadTickStats() // Senza parametri carica l'ultimo tick
        autoRefresh.value = true // Attiva automaticamente l'auto refresh per i tick
      }
    }

    const changeTick = (delta) => {
      const newTick = currentTick.value + delta
      if (newTick >= 1) {
        previousTickValue = currentTick.value
        currentTick.value = newTick
        loadTickStats(newTick) // Carica il tick specifico richiesto
      }
    }

    const jumpToLatestTick = () => {
      // Carica l'ultimo tick disponibile
      loadTickStats() // Senza parametri carica l'ultimo tick
    }

    const checkExploitAlerts = async () => {
      if (currentTick.value > 1) {
        checkingAlerts.value = true
        try {
          await manualCheck(currentTick.value, currentTick.value - 1)
        } catch (error) {
          console.error('Error checking for exploit alerts:', error)
        } finally {
          checkingAlerts.value = false
        }
      }
    }

    const onAlertTriggered = (alertData) => {
      console.log('Alert triggered in parent:', alertData)
      // Qui puoi aggiungere logiche aggiuntive quando viene trigggerato un alert
      // ad esempio logging, notifiche push, etc.
    }

    const formatTime = (timestamp) => {
      if (!timestamp) return ''
      const date = new Date(timestamp * 1000)
      return date.toLocaleString()
    }

    const getHeaderClass = (columnName) => {
      if (columnName === 'team') return 'bg-blue-1 text-weight-bold'
      if (columnName === 'total') return 'bg-green-1 text-weight-bold'
      return 'bg-grey-1 text-weight-bold'
    }

    const getRowClass = (rowIndex) => {
      if (viewMode.value === 'overall') {
        // Evidenzia le prime 3 posizioni nella modalità overall
        if (rowIndex === 0) return 'bg-yellow-1' // 1° posto
        if (rowIndex === 1) return 'bg-grey-3'   // 2° posto
        if (rowIndex === 2) return 'bg-orange-2' // 3° posto
      }
      return ''
    }

    const getCellClass = (columnName, value) => {
      const baseClass = 'text-center'
      
      if (columnName === 'team') {
        return baseClass + ' text-weight-bold'
      }
      
      if (columnName === 'total') {
        return baseClass + ' bg-green-1 text-weight-bold'
      }
      
      // Evidenzia le celle con 0 flag rubate
      if (value === 0) {
        return baseClass + ' bg-red-2 text-red-8 text-weight-bold'
      }
      
      return baseClass
    }

    const calculateNextTickTime = () => {
      if (!tickStats.value) return null
      
      const tickDuration = tickStats.value.tick_duration || 120 // 2 minuti di default
      const startTime = tickStats.value.start_time
      const currentTick = tickStats.value.tick
      
      // Calcola quando inizierà il prossimo tick
      const nextTickStartTime = startTime + (currentTick * tickDuration)
      
      return nextTickStartTime * 1000 // Converti in millisecondi per JavaScript
    }

    const startAutoRefresh = () => {
      if (refreshInterval) {
        clearInterval(refreshInterval)
      }

      const refreshFunction = () => {
        const oldTick = currentTick.value
        
        if (viewMode.value === 'overall') {
          loadOverallStats()
        } else {
          loadTickStats().then(() => {
            // Controlla se il tick è cambiato durante l'auto refresh
            if (currentTick.value > oldTick) {
              previousTickValue = oldTick
              console.log(`Tick avanzato automaticamente: ${oldTick} → ${currentTick.value}`)
            }
          })
        }
      }

      // Per la modalità tick, sincronizza con i tick reali
      if (viewMode.value === 'tick') {
        const nextTickTime = calculateNextTickTime()
        
        if (nextTickTime) {
          const now = Date.now()
          const timeUntilNextTick = nextTickTime - now
          
          if (timeUntilNextTick > 0) {
            // Avvia il primo refresh quando inizia il prossimo tick
            setTimeout(() => {
              refreshFunction()
              // Poi continua con refresh ogni 2 minuti (tick duration)
              refreshInterval = setInterval(refreshFunction, (tickStats.value?.tick_duration || 120) * 1000)
            }, timeUntilNextTick)
            
            console.log(`Auto refresh sincronizzato: prossimo aggiornamento in ${Math.round(timeUntilNextTick / 1000)} secondi`)
          } else {
            // Se siamo già nel tick corrente, inizia subito e poi ogni tick duration
            refreshFunction()
            refreshInterval = setInterval(refreshFunction, (tickStats.value?.tick_duration || 120) * 1000)
          }
        } else {
          // Fallback: refresh ogni 30 secondi se non riusciamo a calcolare il timing
          refreshInterval = setInterval(refreshFunction, 30000)
        }
      } else {
        // Per la modalità overall, usa refresh ogni 30 secondi
        refreshInterval = setInterval(refreshFunction, 30000)
      }
    }

    const stopAutoRefresh = () => {
      if (refreshInterval) {
        clearInterval(refreshInterval)
        refreshInterval = null
      }
    }

    // Watch per auto refresh
    watch(autoRefresh, (newValue) => {
      if (newValue) {
        startAutoRefresh()
      } else {
        stopAutoRefresh()
      }
    })

    // Watch per riavviare auto refresh quando cambiano i dati del tick (per ricalcolare timing)
    watch(() => tickStats.value?.tick, (newTick, oldTick) => {
      if (autoRefresh.value && viewMode.value === 'tick' && newTick !== oldTick) {
        console.log('Tick cambiato, riavvio auto refresh sincronizzato')
        startAutoRefresh()
      }
    })

    // Watch per cambiamenti del tick per triggerare gli alert automatici
    watch(() => currentTick.value, (newTick, oldTick) => {
      if (viewMode.value === 'tick' && newTick && oldTick && newTick > oldTick) {
        previousTickValue = oldTick
      }
    })

    onMounted(() => {
      // Carica le statistiche generali di default
      loadOverallStats()
    })

    onUnmounted(() => {
      stopAutoRefresh()
    })

    return {
      viewMode,
      overallStats,
      tickStats,
      currentStats,
      loading,
      currentTick,
      autoRefresh,
      checkingAlerts,
      exploitAlerts,
      columns,
      tableRows,
      loadOverallStats,
      loadTickStats,
      onViewModeChange,
      changeTick,
      jumpToLatestTick,
      checkExploitAlerts,
      onAlertTriggered,
      formatTime,
      getHeaderClass,
      getRowClass,
      getCellClass
    }
  }
}
</script>

<style scoped>
.stats-table-container {
  border-radius: 8px;
  overflow: hidden;
}

.stats-table {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stats-table .q-table__container {
  border-radius: 8px;
}

.stats-table td, .stats-table th {
  border-right: 1px solid #e0e0e0;
}

.stats-table th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.zero-flags {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 1;
  }
}

.legend-box {
  width: 20px;
  height: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* Stili per evidenziare le posizioni nella classifica */
.bg-yellow-1 {
  background-color: #fff9c4 !important; /* 1° posto - oro */
}

.bg-grey-3 {
  background-color: #e0e0e0 !important; /* 2° posto - argento */
}

.bg-orange-2 {
  background-color: #ffcc80 !important; /* 3° posto - bronzo */
}

/* Migliora la leggibilità del testo sugli sfondi colorati */
.bg-yellow-1 .q-td,
.bg-grey-3 .q-td,
.bg-orange-2 .q-td {
  font-weight: 600;
}
</style>
