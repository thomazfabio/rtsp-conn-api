<template>
  <v-container>
    <v-row>
      <v-col cols="12" lg="4" md="6">
        <visualizeCamV2 />
      </v-col>
      <v-col cols="12" lg="4" md="6">
        <visualizeCamV2 />
      </v-col>
      <v-col cols="12" lg="4" md="6">
        <visualizeCamV2 />
      </v-col>

      <v-col cols="12" lg="4" md="6">
        <visualizeCamV2 />
      </v-col>

      <v-col cols="12" lg="4" md="6">
        <visualizeCamV2 />
      </v-col>
      <v-col cols="12" lg="4" md="6">
        <visualizeCamV2 />
      </v-col>
      <v-col cols="12" lg="4" md="6">
        <playerStreamV2 />
      </v-col>
    </v-row>
  </v-container>
</template>
<script setup>
import visualizeCamV2 from '../components/manageCam/visualizeCamV2.vue';
import playerStreamV2 from '../components/manageCam/playerStreamV2.vue';
</script>