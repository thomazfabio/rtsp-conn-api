<template>
  <v-stepper  :items="['Passo 1', 'Step 2', 'Step 3', 'Step 4']">
    <template  v-slot:item.1>
      <v-card title="Selecione o tipo de dispositivo:" flat>
        <v-row>
          <v-col cols="6">
        <v-select
          label="Selecione o tipo de dispositivo que deseja conectar"
          :items="[
            'DVR',
            'Camera IP', 
            'URL da Web',
            'Inserir manualmente',
            'Outro',
          ]"
          variant="outlined"
          @update:modelValue="$emit('device', $event)" 
         
        ></v-select>
      </v-col>
      </v-row>
      <v-row>
      </v-row>
      </v-card>
    </template>

    <template v-slot:item.2>
      <v-card title="Step Two" flat>...</v-card>
    </template>

    <template v-slot:item.4>
      <v-card title="Step Three" flat>...</v-card>
    </template>
  </v-stepper>
</template>

<script setup>

</script>
