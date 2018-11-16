

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
            <tr>
              <th scope="col">Submission Time</th>
              <th scope="col">Status</th>
              <th scope="col">Progress</th>
              <th scope="col">Source</th>
              <th scope="col">Output</th>
              <th scope="col">Priority</th>
              <th scope="col">End Time</th>
              <th scope="col">Job ID</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
           <tr v-for="(job, index) in jobs" :key="index">
              <td>{{ job.Submit_Time }}</td>
              <td v-if="job.Status == 'running'" class="text-warning">{{ job.Status }}</td>
              <td v-else-if="job.Status == 'errored'" class="text-danger">{{ job.Status }}</td>
              <td v-else class="text-success">{{ job.Status }}</td>
              <td>
              <div class="progress">
              <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" :aria-valuenow="job.Progress" aria-valuemin="0" aria-valuemax="100" :style="{'width': `${job.Progress}%`}">
              {{ job.Progress }}%
              </div>
              </div>
              </td>
              <td>{{ job.Source}}</td>
              <td>{{ job.Output }}</td>
              <td>{{ job.Priority }}</td>
              <td>{{ job.End_Time}}</td>
              <td>{{ job.JobID}}</td>
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
                    label="Title:"
                    label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addJobForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                      label="Author:"
                      label-for="form-author-input">
            <b-form-input id="form-author-input"
                          type="text"
                          v-model="addJobForm.author"
                          required
                          placeholder="Enter author">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-read-group">
          <b-form-checkbox-group v-model="addJobForm.read" id="form-checks">
            <b-form-checkbox value="true">Read?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
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
        const path = 'http://localhost:5000/books';
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
        this.addJobForm.title = '';
        this.addJobForm.author = '';
        this.addJobForm.read = [];
    },
    onSubmit(evt) {
        evt.preventDefault();
        this.$refs.addJobModal.hide();
        let read = false;
        if (this.addJobForm.read[0]) read = true;
        const payload = {
          title: this.addJobForm.title,
          author: this.addJobForm.author,
          read, // property shorthand
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
