

<template class="bg-dark">
  <div class="container-fluid">
    
    <!-- Navbar -->
    <div>
      <nav class="navbar navbar-light" style="background-color: #2c3034;">
        <a class="navbar-brand mb-0 h1" href="#" style="color: #fff">
          <img src="/docs/4.0/assets/brand/bootstrap-solid.svg" width="30" height="30" class="d-inline-block align-top" alt="">
          FTC Jobs
        </a>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.job-modal>Add Job</button>
      </nav>
    </div>

    <div class="row">
      <div class="col-sm-12">
        <!-- job board display -->


        <br><br>
        <table class="table table-hover table-dark table-striped table-hover table-sm">
          <thead>
            <tr class="d-flex">
              <th  class="col-sm-1 "scope="col">Submission Time</th>
              <th  class="col-1" scope="col">Status</th>
              <th  class="col-1" scope="col">Progress</th>
              <th  class="col-2" scope="col">Source</th>
              <th  class="col-2" scope="col">Output</th>
              <th  class="col-1" scope="col">Priority</th>
              <th  class="col-1" scope="col">End Time</th>
              <!-- <th  class="col-1" scope="col">Job ID</th> -->
              <th></th>
            </tr>
          </thead>
          <tbody>
           <tr class="d-flex" v-for="(job, index) in jobs" :key="index">
              <td class="col-sm-1">{{ job.Submit_Time }}</td>
              <td  v-if="job.Status == 'running'" class="text-warning col-1">{{ job.Status }}</td>
              <td v-else-if="job.Status == 'errored'" class="text-danger col-1">{{ job.Status }}</td>
              <td v-else class="text-success col-1">{{ job.Status }}</td>
              <td class="col-1">
              <div class="progress">
              <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" :aria-valuenow="job.Progress" aria-valuemin="0" aria-valuemax="100" :style="{'width': `${job.Progress}%`}">
              {{ job.Progress }}%
              </div>
              </div>
              </td>
              <td class="col-2" style="white-space: nowrap; overflow:hidden; text-overflow: ellipsis;">{{ job.Source}}</td>
              <td class="col-2" style="white-space: nowrap; overflow:hidden; text-overflow: ellipsis;">{{ job.Output }}</td>
              <td class="col-1">{{ job.Priority }}</td>
              <td class="col-1">{{ job.End_Time}}</td>
              <!-- <td class="col-1">{{ job.JobID}}</td> -->
              <td>
                <button type="button" class="btn btn-danger btn-sm" @click="onDeleteJob(job)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>


    <!-- New job modal -->
      <b-modal ref="addJobModal"
            id="job-modal"
            title="Add a new job"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group"
                    label="Source file:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        accept=".ts, .mxf, .mov"
                        v-model="addJobForm.sourceFile"
                        :state="Boolean(addJobForm.sourceFile)"
                        required
                        placeholder="Select file to transcode">
          </b-form-input>
          <p>Selected file: {{addJobForm.sourceFile}}</p>
        </b-form-group>
        <b-form-group id="form-author-group"
                      label="Author:"
                      label-for="form-author-input">
            <b-form-input id="form-author-input"
                          type="text"
                          v-model="addJobForm.outputFolder"
                          placeholder="Enter destination folder">
            </b-form-input>
            <p>Selected folder: {{addJobForm.outputFolder}}</p>
          </b-form-group>
        <b-form-group id="form-read-group">
          <b-form-checkbox-group v-model="addJobForm.read" id="form-checks">
            <b-form-checkbox value="true">Read?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
            <b-form-select v-model="addJobForm.SelectedPreset">
                <option :value="null">Please select an option</option>
                <option value="preset1">Preset 1</option>
                <option value="preset2">Preset 2</option>
            </b-form-select>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>


  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      jobs: [],
      addJobForm: {
        title: '',
        author: '',
        read: [],
      },
    };
  },
  methods: {
    // get jobs
    getJobs() {
      const path = 'http://localhost:5001/jobs';

      setInterval(() => {
       axios.get(path)
        .then((res) => {
          this.jobs = res.data.jobs;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      }, 30000);
    },
    // add jobs
    addJob(payload) {
        const path = 'http://localhost:5001/jobs';
        axios.post(path, payload)
          .then(() => {
            this.getJobs();
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.log(error);
            this.getJobs();
          });
      },
    initForm() {
        this.addJobForm.sourceFile = '';
        this.addJobForm.outputFolder = '';
        // this.addJobForm.read = [];
        this.addJobForm.SelectedPreset = "";
    },
    onSubmit(evt) {
        evt.preventDefault();
        this.$refs.addJobModal.hide();
        let read = false;
        if (this.addJobForm.read[0]) read = true;
        const payload = {
          source: this.addJobForm.sourceFile,
          output: this.addJobForm.outputFolder,
          read, // property shorthand
          preset: this.addJobForm.SelectedPreset,
        };
        this.addJob(payload);
        this.initForm();
    },
    onReset(evt) {
        evt.preventDefault();
        this.$refs.addJobModal.hide();
        this.initForm();
    },
    // delete jobs
    removeJob(JobID) {
    const path = `http://localhost:5001/jobs/${JobID}`;
    axios.delete(path)
      .then(() => {
        this.getJobs();
        this.message = 'Job removed!';
        this.showMessage = true;
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        this.getJobs();
      });
    },
    onDeleteJob(job) {
      this.removeJob(job.JobID);
    },

  },
  created() {
    this.getJobs();
  },
};
</script>
