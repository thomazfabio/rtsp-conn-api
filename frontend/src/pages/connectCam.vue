<template>
  <v-container>
    
    <v-row class="d-flex justify-center">
      <v-col cols="12" xl="8">
        <v-card>
          <v-card-title>
            <h4 >Assistênte para conectar câmera</h4>
          </v-card-title>
          <v-card-text>
            <p style="text-align: justify;">
              Para se conectar a uma câmera, você precisa fornecer o IP da câmera
              endereço, nome de usuário e senha.
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row class="d-flex justify-center">
      <v-col cols="12" xl="8">
        <ConnectAddCam/>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import ConnectAddCam from "../components/ConnectAddCAM.vue";
import { ref, watch } from "vue";
</script>
