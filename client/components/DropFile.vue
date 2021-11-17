<template>
    <v-card
        @drop.prevent="onDrop($event)"
        @dragover.prevent="dragover = true"
        @dragenter.prevent="dragover = true"
        @dragleave.prevent="dragover = false"
        :class="{ 'grey lighten-2': dragover }"
    > <p class="font-weight-black text-center">{{title}}</p>
      <v-sheet height="100%" class="transparent d-flex align-center justify-center">
        <v-img max-width="180" v-if="file" :src="file"/>
        <v-card-text v-else>
        <v-row class="d-flex flex-column" dense align="center" justify="center">
            <v-icon :class="[dragover ? 'mt-2, mb-6' : 'mt-5']" size="60">
            {{icon}}
            </v-icon>
            <p>Drop your file(s) here.</p>
          
            <p v-if="enterName==='false'">{{desc}}</p>
            <v-text-field 
              v-model="fileName"
              hint="Enter FileName First"
              persistent-hint
              clearable 
              v-else
            ></v-text-field>
        </v-row>
        </v-card-text>
        <v-card-actions>
        <v-spacer></v-spacer>
        </v-card-actions>
      </v-sheet>
    </v-card>
</template>

<script>
export default {
  name: "Upload",
  props: {
    title: {
      type: String,
      required: true,
    },
    url: {
      type: String,
      required: true
    },
    showImg: {
      type: String,
      required: true,
    },
    enterName: {
      type: String,
      required: true,
    },
    icon: {
      type: String,
      required: true
    },
    desc: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      dragover: false,
      file: '',
      fileName: '',
      dialog: '',
    };
  },
  methods: {
    onDrop(e) {
      const formData = new FormData();
      const img = e.dataTransfer.files[0];
      const url = this.$props.url;
      const prevThis = this;

      formData.append('image', img);
      
      if (this.$props.showImg === 'true'){
        this.file = URL.createObjectURL(img);
      }

      if (this.$props.enterName === 'true'){
        if (this.fileName === '') {
          alert("Enter fileName First!");
          return;
        }
        formData.append('name', this.fileName);
      }
      
      this.dragover = false;
      this.$axios.post(url,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        },
      ).then(() => {
        console.log('SUCCESS!!');
        prevThis.$emit("upload", img);
        prevThis.fileName = '';
      }).catch(() => {
        console.log('FAILURE!!');
      });
    }
  }
};
</script>

<style scoped></style>