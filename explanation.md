The load balancer was not being configured with the '10-first-minutes' role, which is responsible for setting up the 'deploy' user and SSH access. This was because the load balancer was not part of the 'devops' group in your Ansible inventory.

I have updated `ansible/hosts` to include `loadbalancer.osay21.me` in the `[devops]` group.

**Next Steps:**

1.  **Re-run your Ansible playbook:** You need to re-run your main Ansible playbook (e.g., `ansible-playbook ansible/site.yml`) to apply these changes to your load balancer.
2.  **SSH as the 'deploy' user:** Once the playbook has successfully run, you should be able to SSH into your load balancer using the `deploy` user and the private key corresponding to `/home/carloscarmarcus/.ssh/devops.pub`.

Example SSH command:
`ssh -i /home/carloscarmarcus/.ssh/devops loadbalancer.osay21.me -l deploy`