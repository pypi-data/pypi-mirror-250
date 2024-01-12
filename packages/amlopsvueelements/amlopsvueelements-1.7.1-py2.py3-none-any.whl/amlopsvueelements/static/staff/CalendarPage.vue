<script setup lang="ts">
import { ref, reactive, watchEffect, watch } from 'vue'

import moment from 'moment-timezone'
import type { CalendarOptions } from '@fullcalendar/core'
import FullCalendar from '@fullcalendar/vue3'
import bootstrap5Plugin from '@fullcalendar/bootstrap5'
import resourceTimelinePlugin from '@fullcalendar/resource-timeline'
import rrulePlugin from '@fullcalendar/rrule'
import momentPlugin from '@fullcalendar/moment'
import momentTimezone from '@fullcalendar/moment-timezone'
import interactionPlugin from '@fullcalendar/interaction'

import EditEventModal from '@/components/calendar/EditEventModal.vue'
import { SelectField } from 'shared/components'

import type { Team } from '@/models/Team'
import eventService from '@/services/EventService'
import { useTimezones } from '@/composables/useTimezones'
import { useTeams } from '@/composables/useTeams'

const calendar = ref()
const isCalendarMounted = ref(false)
const isEditEventModalOpen = ref(false)
const selectedTimezone = ref({
  label: 'UTC',
  value: 'UTC'
})
const selectedTeams = ref<Team[]>([])

const { data: timezones, isLoading: isLoadingTimezones } = useTimezones()
const { data: teams, isLoading: isLoadingTeams } = useTeams()

const calendarOptions = reactive<CalendarOptions>({
  plugins: [
    bootstrap5Plugin,
    resourceTimelinePlugin,
    rrulePlugin,
    momentPlugin,
    momentTimezone,
    interactionPlugin
  ],
  schedulerLicenseKey: 'CC-Attribution-NonCommercial-NoDerivatives',
  themeSystem: 'bootstrap5',
  initialView: 'resourceTimelineDay',
  height: '100%',
  customButtons: {
    addEvent: {
      text: 'Add Calendar Event',
      click() {
        isEditEventModalOpen.value = true
      }
    },
    quickAddSicknessAbsence: {
      text: 'Quick-Add Sickness Absence'
    },
    timezoneSelect: {
      text: ''
    }
  },
  headerToolbar: {
    right:
      'timezoneSelect addEvent quickAddSicknessAbsence resourceTimelineMonth,resourceTimelineWeek,resourceTimelineDay prev,today,next'
  },
  resourceAreaHeaderClassNames: 'custom-resource-area-header',
  resourceGroupField: 'groupId',
  resourceLabelClassNames: 'centered-resource-label',
  resources: [],
  events: (info, successCallback, failureCallback) => {
    const selectedTeamNames = selectedTeams.value?.map((team) => team.name)
    eventService
      .fetchEvents(info.start, info.end, selectedTeamNames)
      .then(({ events, resources }) => {
        successCallback(events)
        calendarOptions.resources = resources
      })
      .catch(failureCallback)
  },
  selectable: true,
  selectMirror: true,
  viewDidMount: () => {
    // Patch timezone select target in header toolbar
    const timezoneSelectButton = document.querySelector(
      '.fc-header-toolbar button.fc-timezoneSelect-button'
    )
    if (!timezoneSelectButton) {
      return
    }

    timezoneSelectButton.setAttribute('style', 'display: none;')

    const element = document.createElement('div')
    element.className = 'timezoneSelect-target'
    timezoneSelectButton.parentElement?.prepend(element)

    isCalendarMounted.value = true
  }
})

watch([selectedTeams, calendar], () => {
  const calendarApi = calendar.value?.getApi()
  calendarApi && calendarApi.refetchEvents()
})
watchEffect(() => {
  calendarOptions.timeZone = selectedTimezone.value.value
})
</script>
<template>
  <div class="h-full">
    <FullCalendar ref="calendar" :options="calendarOptions">
      <template v-slot:resourceAreaHeaderContent>
        <SelectField
          :options="teams"
          label="name"
          :loading="isLoadingTeams"
          v-model="selectedTeams"
          multiple
          :taggable="true"
          placeholder="Teams Selection"
          class="mb-0"
        />
      </template>
      <template v-slot:eventContent="arg">
        <div class="text-center">
          <b>{{ arg.event.title }}</b>
          <div v-if="arg.view.type !== 'resourceTimelineMonth'">
            <template v-if="arg.event.allDay"> All Day </template>
            <template v-else>
              {{
                moment(arg.event.start)
                  .tz(
                    selectedTimezone.value === 'local' ? moment.tz.guess() : selectedTimezone.value
                  )
                  .format('HH:mm')
              }}
              -
              {{
                moment(arg.event.end)
                  .tz(
                    selectedTimezone.value === 'local' ? moment.tz.guess() : selectedTimezone.value
                  )
                  .format('HH:mm')
              }}
              {{ selectedTimezone.label }}
              (
              {{ moment.duration(arg.event.end).subtract(arg.event.start).hours() }}h
              {{ moment.duration(arg.event.end).subtract(arg.event.start).minutes() }}m )
            </template>
          </div>
        </div>
      </template>
      <template v-slot:resourceLabelContent="arg">
        <div class="text-center">
          <b>{{ arg.resource.title }}</b>
          <div>({{ arg.resource.extendedProps.role }})</div>
        </div>
      </template>
    </FullCalendar>
    <Teleport to=".fc-header-toolbar .timezoneSelect-target" v-if="isCalendarMounted">
      <div class="timezone-select-container">
        <SelectField
          :options="timezones"
          label="label"
          :loading="isLoadingTimezones"
          v-model="selectedTimezone"
          :clearable="false"
          :append-to-body="false"
          placeholder="Timezone Selection"
          class="mb-0"
        />
      </div>
    </Teleport>

    <EditEventModal v-model:open="isEditEventModalOpen" :event="{}" />
  </div>
</template>

<style scoped lang="scss">
.timezone-select-container {
  width: 300px;
}

.vs__clear {
  top: 0;
}
</style>
