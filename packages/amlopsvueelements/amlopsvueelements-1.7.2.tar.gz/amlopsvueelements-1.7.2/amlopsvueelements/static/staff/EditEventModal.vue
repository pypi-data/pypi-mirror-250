<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
// @ts-ignore
import { useVuelidate } from '@vuelidate/core'
import { required } from '@vuelidate/validators'
import type { AxiosError } from 'axios'
import moment from 'moment'
import { useMutation } from '@tanstack/vue-query'

import {
  BModal,
  BButton,
  BForm,
  BFormGroup,
  BFormInvalidFeedback,
  BAlert
} from 'bootstrap-vue-next'
import { FlatPickr, SelectField } from 'shared/components'
import ApplyDatesSelect from '@/components/common/ApplyDatesSelect.vue'

import type { Person } from '@/models/Person'
import type { SpecificEntryPayload } from '@/models/Entry'
import type { EntryType } from '@/models/EntryType'
import { usePeople } from '@/composables/usePeople'
import { useEntryTypes } from '@/composables/useEntryTypes'

import entryService from '@/services/EntryService'

interface Form {
  person: Person | undefined
  start_date: string | undefined
  start_hour: string | undefined
  end_date: string | undefined
  end_hour: string | undefined
  applied_on_dates: number[] | undefined
  entry_type: EntryType | undefined
}

const open = defineModel<boolean>('open')
const emit = defineEmits(['event-created'])

const { data: people, isLoading: isLoadingPeople } = usePeople()
const { data: entryTypes, isLoading: isLoadingEntryTypes } = useEntryTypes()

const { isPending, mutate } = useMutation({
  mutationFn: (entries: SpecificEntryPayload[]) => entryService.createSpecificEntries(entries),
  onSuccess: (data) => {
    emit('event-created', data)
    open.value = false
  },
  onError: (error: AxiosError) => {
    if (!error.response) {
      non_field_errors.value = ['Network error']
      return
    }

    const errors = (error.response.data as any).errors
      ? (error.response.data as any).errors[0]
      : undefined
    if (!errors) {
      non_field_errors.value = ['Unknown error']
    } else if (errors.non_field_errors) {
      non_field_errors.value = errors.non_field_errors
    } else if (errors.message) {
      non_field_errors.value = [errors.message]
    } else {
      $externalResults.value = errors
    }
  }
})

const non_field_errors = ref<string[]>([])
const $externalResults = ref({})
const rules = computed(() => ({
  person: { required },
  start_hour: { required },
  end_hour: { required },
  start_date: { required },
  end_date: { required },
  applied_on_dates: { required },
  entry_type: { required }
}))
const values = reactive<Form>({
  person: undefined,
  start_date: '',
  start_hour: '',
  end_date: '',
  end_hour: '',
  applied_on_dates: [],
  entry_type: undefined
})
const v$ = useVuelidate(rules, values, { $externalResults, $autoDirty: true })

const timePeriodDescription = computed(() => {
  const start_hour_utc = values.start_hour
    ? moment().startOf('day').add(values.start_hour).tz('utc')
    : undefined
  const end_hour_utc = values.end_hour
    ? moment().startOf('day').add(values.end_hour).tz('utc')
    : undefined

  return start_hour_utc || end_hour_utc
    ? `${start_hour_utc ? start_hour_utc.format('HH:mm UTC') : ''} - ${
        end_hour_utc ? end_hour_utc.format('HH:mm UTC') : ''
      }`
    : ''
})

const onSubmit = async () => {
  const isValid = await v$?.value?.$validate()
  non_field_errors.value = []

  if (!isValid) {
    return
  }

  const payload = [
    {
      person: values.person?.person_id,
      team: values.person?.team_id,
      start_date: values.start_date,
      start_hour: values.start_hour,
      end_date: values.end_date,
      end_hour: values.end_hour,
      applied_on_dates: values.applied_on_dates,
      entry_type: values.entry_type?.id
    }
  ]
  mutate(payload)
}

const onCancel = () => {
  open.value = false
}

const resetForm = () => {
  values.person = undefined
  values.start_date = ''
  values.start_hour = ''
  values.end_date = ''
  values.end_hour = ''
  values.applied_on_dates = []
  values.entry_type = undefined

  v$.value.$reset()
}

watch(values, () => {
  non_field_errors.value = []
})
watch(open, () => {
  if (open.value) {
    resetForm()
  }
})
</script>

<template>
  <BModal v-model="open" :no-close-on-backdrop="isPending" title="Add Calendar Event" centered>
    <BForm>
      <BAlert
        :model-value="true"
        variant="danger"
        class="mb-[1rem]"
        v-for="error of non_field_errors"
        :key="error"
        >{{ error }}</BAlert
      >

      <BFormGroup label="Team Member:" class="mb-[1rem]" :state="!v$.person.$error">
        <SelectField
          :loading="isLoadingPeople"
          :options="people"
          label="name"
          v-model="values.person"
          required
          :clearable="true"
          :append-to-body="false"
          class="mb-0"
        />
        <BFormInvalidFeedback :state="!v$.person.$error">
          <div v-for="error of v$.person.$errors" :key="error.$uid">{{ error.$message }}</div>
        </BFormInvalidFeedback>
      </BFormGroup>
      <BFormGroup
        label="Time Period:"
        :description="timePeriodDescription"
        class="mb-[1rem]"
        :state="v$.start_hour.$error || v$.end_hour.$error"
      >
        <div class="flex gap-x-2">
          <FlatPickr
            :config="{
              noCalendar: true,
              enableTime: true,
              dateFormat: 'H:i',
              time_24hr: true
            }"
            v-model="values.start_hour"
            placeholder="Select a time"
          />
          <FlatPickr
            :config="{
              noCalendar: true,
              enableTime: true,
              dateFormat: 'H:i',
              time_24hr: true,
              position: 'auto right',
              minTime: values.start_hour
            }"
            v-model="values.end_hour"
            placeholder="Select a time"
          />
        </div>
        <BFormInvalidFeedback :state="!v$.start_hour.$error">
          <div v-for="error of v$.start_hour.$errors" :key="error.$uid">
            {{ error.$message }}
          </div>
        </BFormInvalidFeedback>
        <BFormInvalidFeedback :state="!v$.end_hour.$error">
          <div v-for="error of v$.end_hour.$errors" :key="error.$uid">
            {{ error.$message }}
          </div>
        </BFormInvalidFeedback>
      </BFormGroup>
      <BFormGroup
        label="Recurring:"
        class="mb-[1rem]"
        :state="v$.start_date.$error || v$.end_date.$error"
      >
        <div class="flex gap-x-2">
          <FlatPickr v-model="values.start_date" />
          <FlatPickr
            :config="{
              minDate: values.start_date
            }"
            v-model="values.end_date"
          />
        </div>
        <BFormInvalidFeedback :state="!v$.start_date.$error">
          <div v-for="error of v$.start_date.$errors" :key="error.$uid">
            {{ error.$message }}
          </div>
        </BFormInvalidFeedback>
        <BFormInvalidFeedback :state="!v$.end_date.$error">
          <div v-for="error of v$.end_date.$errors" :key="error.$uid">
            {{ error.$message }}
          </div>
        </BFormInvalidFeedback>
      </BFormGroup>
      <BFormGroup label="Applicable Dates:" class="mb-[1rem]" :state="v$.applied_on_dates.$error">
        <ApplyDatesSelect
          v-model="values.applied_on_dates"
          :start_date="values.start_date"
          :end_date="values.end_date"
          :disabled="!values.start_date || !values.end_date"
        />
        <BFormInvalidFeedback :state="!v$.applied_on_dates.$error">
          <div v-for="error of v$.applied_on_dates.$errors" :key="error.$uid">
            {{ error.$message }}
          </div>
        </BFormInvalidFeedback>
      </BFormGroup>
      <BFormGroup label="Event Type:" class="mb-[1rem]" :state="v$.entry_type.$error">
        <SelectField
          :loading="isLoadingEntryTypes"
          :options="entryTypes"
          label="name"
          v-model="values.entry_type"
          :clearable="false"
          :append-to-body="false"
          class="mb-0"
        />
        <BFormInvalidFeedback :state="!v$.entry_type.$error">
          <div v-for="error of v$.entry_type.$errors" :key="error.$uid">{{ error.$message }}</div>
        </BFormInvalidFeedback>
      </BFormGroup>
    </BForm>

    <template v-slot:ok>
      <BButton type="submit" :disabled="isPending" variant="primary" @click="onSubmit"
        >Submit</BButton
      >
    </template>
    <template v-slot:cancel>
      <BButton type="button" @click="onCancel">Cancel</BButton>
    </template>
  </BModal>
</template>

<style scoped lang="scss"></style>
