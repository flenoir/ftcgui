

<template class="bg-dark">
  <div class="container-fluid">
    
    <!-- Navbar -->
    <div>
      <nav class="navbar navbar-light" style="background-color: #2c3034;">
        <a class="navbar-brand mb-0 h1" href="#" style="color: #fff">
          <img src="/docs/4.0/assets/brand/bootstrap-solid.svg" width="30" height="30" class="d-inline-block align-top" alt="">
          FTC Jobs
        </a>
        <button type="button" class="btn btn-success btn-sm">Add Job</button>
      </nav>
      <!-- <br><br> -->
    </div>

    <div class="row">
      <div class="col-sm-12">
        <!-- <h1 class="text-light">Jobs</h1> -->
        <!-- <hr><br><br> -->
        <!-- <button type="button" class="btn btn-success btn-sm">Add Job</button> -->
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
              <th></th>
            </tr>
          </thead>
          <tbody>
           <tr v-for="(job, index) in jobs" :key="index">
              <td>{{ job.Submit_Time }}</td>
              <td v-if="job.Status == 'running'" class="text-warning">{{ job.Status }}</td>
              <td v-else-if="job.Status == 'errored'" class="text-danger">{{ job.Status }}</td>
              <td v-else class="text-success">{{ job.Status }}</td>
              <td>{{ job.Progress }}</td>
              <td>{{ job.Source}}</td>
              <td>{{ job.Output }}</td>
              <td>{{ job.Priority }}</td>
              <td>{{ job.End_Time}}</td>
              <!-- <td>
                <span v-if="job.read">Yes</span>
                <span v-else>No</span>
              </td> -->
              <td>
                <!-- <button type="button" class="btn btn-warning btn-sm">Update</button> -->
                <button type="button" class="btn btn-danger btn-sm">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      jobs: [],
    };
  },
  methods: {
    getJobs() {
      const path = 'http://localhost:5001/jobs';
    //    setInterval(() => {
    //    axios.get(path)
    //     .then((res) => {
    //       this.jobs = res.data.jobs;
    //     })
    //     .catch((error) => {
    //       // eslint-disable-next-line
    //       console.error(error);
    //     });
    // }, 30000)
      axios.get(path)
        .then((res) => {
          this.jobs = res.data.jobs;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getJobs();
  },
};
</script>
