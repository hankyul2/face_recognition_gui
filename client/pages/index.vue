<template>
  <div>
  <v-container>
    <v-row>
      <v-col>
        <Upload 
          title="Target Face Image"
          url="/api/recognition/register" 
          showImg="true"
          enterName="false"
          icon="mdi-face-recognition"
          desc="Upload image to compare"
          @upload="targetUpload"
        ></Upload>
      </v-col>
      <v-col>
        <Upload 
          title="Add face to DB"
          url="/api/faceDB/register" 
          showImg="false"
          enterName="true"
          icon="mdi-cloud-upload" 
          desc="Upload image to faceDB"
          @upload="fetchImage"
        ></Upload>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-card class="pa-5">
          <p class="font-weight-black text-center">
            Identification
            <v-btn icon outlined @click="identification">
              <v-icon>mdi-reload</v-icon>
            </v-btn>
          </p>

          <div class="d-flex align-center justify-center">
            <v-img max-height="200" v-if="id_result" :src="id_result.url"></v-img>
            <v-icon size="60" v-else>mdi-account-question</v-icon>
          </div>

          <p class="font-weight-bold text-center pt-5">
            {{identification_result_description}}
          </p>
        </v-card>

        <v-card class="pa-5 mt-5">
          <p class="font-weight-black text-center">
            Verification
            <v-btn icon outlined @click="verification">
              <v-icon>mdi-reload</v-icon>
            </v-btn>
          </p>

          <v-row>
            <v-col>
              <div class="d-flex align-center justify-center">
                <v-img v-if="target_img" :src="target_img" max-width="180"/>
                <v-icon v-else size="60">mdi-account-question</v-icon>
              </div>
            </v-col>
            <v-col>
              <div class="d-flex align-center justify-center">
                <v-img v-if="verification_img" :src="verification_img.url" max-width="180"/>
                <v-icon v-else size="60">mdi-account-question</v-icon>
              </div>
            </v-col>
          </v-row>

          <p class="font-weight-bold text-center pt-5">
            {{verification_result_description}}
          </p>
        </v-card>
      </v-col>

      <v-col>
        <v-card>
          <p class="font-weight-black text-center">
          FaceDB
          <v-btn icon outlined @click="removeAll">
            <v-icon>mdi-trash-can-outline</v-icon>
          </v-btn>
          </p>
          <v-virtual-scroll
            height="400"
            item-height="150"
            :items="facedb"
          >
            <template v-slot:default="{ item }">
              <v-list-item>
                <v-list-item-avatar size="150">
                  <v-img max-height="150" :src="item.url"/>
                </v-list-item-avatar>

                <v-list-item-content>
                  <v-list-item-title>
                    <p class="text-h6">
                      {{ item.name }}
                    </p>
                  </v-list-item-title>
                </v-list-item-content>

                <v-list-item-action>
                  <v-btn depressed small @click="selectVerImage(item)">
                    Select Person
                    <v-icon
                      color="orange darken-4"
                      right
                    >
                      mdi-check-outline
                    </v-icon>
                  </v-btn>
                </v-list-item-action>
              </v-list-item>
            </template>
          </v-virtual-scroll>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
  </div>
</template>

<script>
import Upload from '~/components/DropFile.vue'

export default {
  components: {
    Upload,
  },
  mounted() {
    this.fetchImage();
  },
  data() {
    return {
      url: null,
      image: null,
      id_result: null,
      ver_result: null,
      target_img: '',
      verification_img: '',
      facedb: [],
    }
  },
  computed: {
    identification_result_description() {
      if (this.id_result === null) {
        return '';
      } else {
        return this.id_result.name + '('+ this.id_result.score +')';
      }
    },
    verification_result_description() {
      if (this.ver_result === null) {
        return '';
      } else {
        return this.ver_result.result + '('+ this.ver_result.score +')';
      }
    }
  },
  methods: {
    targetUpload(img) {
      console.log('target upload');
      this.target_img = URL.createObjectURL(img);
    },
    fetchImage(img) {
      const prevThis = this;
      this.$axios.get('/api/faceDB/')
      .then((data) => {
        console.log('SUCCESS!!');
        prevThis.facedb = data.data.body;
        console.log(prevThis.facedb);
      }).catch(() => {
        console.log('FAILURE!!');
      });
    },
    removeAll(e){
      const prevThis = this;
      this.$axios.get('/api/faceDB/remove_all')
      .then((data) => {
        console.log('SUCCESS!!');
        prevThis.fetchImage();
      }).catch(() => {
        console.log('FAILURE!!');
      });
    },
    selectVerImage(e){
      this.verification_img = e;
    },
    identification(){
      const prevThis = this;
      this.$axios.get('/api/recognition/identification')
      .then((data) => {
        console.log('SUCCESS!!');
        console.log(data.data.body);
        prevThis.id_result = data.data.body;
      }).catch(() => {
        console.log('FAILURE!!');
      });
    },
    verification(){
      const prevThis = this;
      this.$axios.get('/api/recognition/verification', 
      {params: {id: prevThis.verification_img.id}})
      .then((data) => {
        console.log('SUCCESS!!');
        console.log(data.data.body);
        prevThis.ver_result = data.data.body;
      }).catch(() => {
        console.log('FAILURE!!');
      });
    },
  }
}
</script>
