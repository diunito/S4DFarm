<template>
  <q-btn 
    icon="settings" 
    flat 
    round 
    size="sm" 
    @click="showSettings = true"
  >
    <q-tooltip>Notification Settings</q-tooltip>
  </q-btn>

  <q-dialog v-model="showSettings">
    <q-card style="min-width: 350px">
      <q-card-section>
        <div class="text-h6">Exploit Alert Settings</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <q-toggle
          v-model="localSettings.enabled"
          label="Enable exploit alerts"
          color="primary"
        />
        
        <q-separator class="q-my-md" />
        
        <div class="text-subtitle2 q-mb-sm">Notification Types</div>
        
        <q-toggle
          v-model="localSettings.showToast"
          :disable="!localSettings.enabled"
          label="Show toast notifications"
          color="primary"
          class="q-mb-sm"
        />
        
        <q-toggle
          v-model="localSettings.showPopup"
          :disable="!localSettings.enabled"
          label="Show popup dialogs"
          color="primary"
          class="q-mb-sm"
        />
        
        <q-toggle
          v-model="localSettings.playSound"
          :disable="!localSettings.enabled"
          label="Play notification sound"
          color="primary"
        />
        
        <q-separator class="q-my-md" />
        
        <div class="text-subtitle2 q-mb-sm">Recent Notifications</div>
        
        <div v-if="recentNotifications.length === 0" class="text-caption text-grey">
          No recent notifications
        </div>
        
        <q-list v-else dense>
          <q-item 
            v-for="notification in recentNotifications" 
            :key="notification.id"
            dense
          >
            <q-item-section>
              <q-item-label caption>
                {{ formatNotificationTime(notification.timestamp) }}
              </q-item-label>
              <q-item-label class="text-body2">
                {{ notification.total_alerts }} alert(s) in tick {{ notification.current_tick }}
              </q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
        
        <q-btn 
          v-if="recentNotifications.length > 0"
          flat 
          size="sm" 
          label="Clear history" 
          @click="clearNotifications"
          class="q-mt-sm"
        />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Test Sound" @click="testSound" :disable="!localSettings.playSound" />
        <q-btn flat label="Cancel" color="primary" @click="cancelSettings" />
        <q-btn flat label="Save" color="primary" @click="saveSettings" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { useExploitNotifications } from '@/composables/useExploitNotifications'

export default {
  name: 'NotificationSettings',
  setup() {
    const showSettings = ref(false)
    const { 
      notificationSettings, 
      updateSettings, 
      getRecentNotifications, 
      clearNotifications 
    } = useExploitNotifications()
    
    const localSettings = ref({ ...notificationSettings.value })
    
    const recentNotifications = computed(() => {
      return getRecentNotifications(5) // Mostra le ultime 5 notifiche
    })
    
    // Sincronizza le impostazioni locali con quelle globali quando si apre il dialog
    watch(showSettings, (isOpen) => {
      if (isOpen) {
        localSettings.value = { ...notificationSettings.value }
      }
    })
    
    const saveSettings = () => {
      updateSettings(localSettings.value)
      showSettings.value = false
    }
    
    const cancelSettings = () => {
      localSettings.value = { ...notificationSettings.value }
      showSettings.value = false
    }
    
    const testSound = () => {
      // Test del suono di notifica
      try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)()
        const oscillator = audioContext.createOscillator()
        const gainNode = audioContext.createGain()
        
        oscillator.connect(gainNode)
        gainNode.connect(audioContext.destination)
        
        oscillator.frequency.value = 800
        oscillator.type = 'sine'
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime)
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5)
        
        oscillator.start(audioContext.currentTime)
        oscillator.stop(audioContext.currentTime + 0.5)
      } catch (error) {
        console.warn('Cannot play test sound:', error)
      }
    }
    
    const formatNotificationTime = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString()
    }
    
    return {
      showSettings,
      localSettings,
      recentNotifications,
      saveSettings,
      cancelSettings,
      testSound,
      clearNotifications,
      formatNotificationTime
    }
  }
}
</script>
