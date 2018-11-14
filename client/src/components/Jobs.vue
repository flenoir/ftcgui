<template class="bg-dark">
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <h1 class="text-light">Jobs</h1>
        <!-- <hr><br><br> -->
        <button type="button" class="btn btn-success btn-sm">Add Job</button>
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
              <td>{{ job.Status }}</td>
              <td>{{ job.Progress }}</td>
              <td>{{ job.Source}}</td>
              <td>{{ job.Output }}</td>
              <td>{{ job.Priority }}</td>
              <td>{{ job.End_Time}}</td>
              <td>
                <span v-if="job.read">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <button type="button" class="btn btn-warning btn-sm">Update</button>
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