<template>
  <div class="jumbotron vertical-center">
    <div class="container">
      <link
        rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/darkly/bootstrap.min.css"
        integrity="sha384-nNK9n28pDUDDgIiIqZ/MiyO3F4/9vsMtReZK39klb/MtkZI3/LtjSjlmyVPS3KdN"
        crossorigin="anonymous"
      />
      <h1>Index page</h1>
      <div class="row">
        <div class="col-sm-12">
          <h3 class="text-success">Settings</h3>
          <hr />
          <!-- Alert -->
          <b-alert variant="success" v-if="showMessage" show>{{
            message
          }}</b-alert>

          <!-- Botones para resetear -->
          <button
            id="resetToDefaultValues"
            type="button"
            class="btn btn-danger btn-sm"
            @click="resetAllSettings"
          >
            Reset All to Default
          </button>
          <br /><br />

          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">Setting</th>
                <th scope="col">Value</th>
                <th scope="col">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(setting, index) in settings" :key="index">
                <td class="text-info">{{ setting.Setting }}</td>
                <td>{{ setting.Value }}</td>
                <td>
                  <div class="btn-group" role="group">
                    <button
                      type="button"
                      class="btn btn-info btn-sm"
                      v-b-modal.setting-update-modal
                      @click="editSetting(setting)"
                    >
                      Update
                    </button>
                    <!-- Botón para resetear un setting individual -->
                    <button
                      id="individualDefault"
                      type="button"
                      class="btn btn-warning btn-sm"
                      @click="resetSetting(setting.id)"
                    >
                      Default
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <!-- Update Setting Modal -->
        <b-modal
          ref="updateSettingModal"
          id="setting-update-modal"
          title="Update"
          hide-backdrop
          hide-footer
        >
          <b-form @submit="onSubmit" @reset="onResetUpdate" class="w-100">
            <b-form-group
              id="form-setting-edit-group"
              label-for="form-setting-edit-input"
            >
              <b-form-input
                id="form-setting-edit-input"
                type="text"
                v-model="editForm.Setting"
                required
                placeholder="Enter new Value"
                readonly
                inactive
                class="bg-transparent border-0 text-white"
              ></b-form-input>
            </b-form-group>
            <b-form-group
              id="form-value-edit-group"
              label-for="form-value-edit-input"
            >
              <b-form-input
                id="form-value-edit-input"
                type="text"
                v-model="editForm.Value"
                required
                placeholder="Enter new Value"
              ></b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary">Submit</b-button>
          </b-form>
        </b-modal>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      settings: [],
      editForm: {
        id: "",
        Setting: "",
        Value: "",
      },
      showMessage: false,
      message: "",
    };
  },
  methods: {
    getSettings() {
      const path = "http://localhost:5000/landing";
      axios
        .get(path)
        .then((res) => {
          this.settings = res.data.settings;
        })
        .catch((err) => {
          console.error(err);
        });
    },

    onSubmit(e) {
      e.preventDefault();
      this.$refs.updateSettingModal.hide();
      const payload = {
        Setting: this.editForm.Setting,
        Value: this.editForm.Value,
      };
      this.updateSetting(payload, this.editForm.id);
    },

    updateSetting(payload, settingID) {
      const path = `http://localhost:5000/landing/${settingID}`;
      axios
        .put(path, payload)
        .then(() => {
          this.getSettings();
          this.message = "Setting Updated";
          this.showMessage = true;
          setTimeout(() => {
            this.showMessage = false;
          }, 2000); // 2000 ms = 2 segundos
        })
        .catch((err) => {
          console.error(err);
        });
    },

    editSetting(setting) {
      this.editForm = setting;
    },

    // Resetear un setting individual a su valor por defecto
    resetSetting(settingID) {
      const path = `http://localhost:5000/landing/${settingID}/reset`;
      axios
        .put(path)
        .then(() => {
          this.getSettings();
          this.message = "Setting Reset to Default";
          this.showMessage = true;
          setTimeout(() => {
            this.showMessage = false;
          }, 2000); // 2000 ms = 2 segundos
        })
        .catch((err) => {
          console.error(err);
        });
    },

    // Resetear todos los settings a sus valores por defecto
    resetAllSettings() {
      const path = "http://localhost:5000/landing/reset";
      axios
        .put(path)
        .then(() => {
          this.getSettings();
          this.message = "All Settings Reset to Default";
          this.showMessage = true;
          setTimeout(() => {
            this.showMessage = false;
          }, 2000); // 2000 ms = 2 segundos
        })
        .catch((err) => {
          console.error(err);
        });
    },

    onResetUpdate() {
      this.editForm = {
        id: "",
        Setting: "",
        Value: "",
      };
    },
  },
  created() {
    this.getSettings();
  },
};
</script>
