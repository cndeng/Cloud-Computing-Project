from boto import exception


class EC2Instance:

    def __init__(self):
        """ Empty EC2Instance Constructor """

    @staticmethod
    def find_instances_running(conn):
        """ Find EC2 Instances """

        # Get all instance reservations associated with this AWS account
        reservations = conn.get_all_reservations()

        result = []
        for res in reservations:
            for instance in res.instances:
                if instance.state == u'running':
                    result.append(instance)

        return result

    @staticmethod
    def find_instances_running_zone(conn, zone):
        """ Find EC2 Instances """

        result = []
        for res in conn.get_all_reservations():
            for instance in res.instances:
                if instance.state == u'running' and instance.placement == zone:
                    result.append(instance)

        return result

    @staticmethod
    def list_instances(conn):
        """ List EC2 Instances """

        # Get all instance reservations associated with this AWS account
        reservations = conn.get_all_reservations()

        # Loop through reservations and extract instance information
        for res in reservations:

            # Loop through the reservation instances and print instance information
            for instance in res.instances:
                # Get instance name from the tags object
                tags = instance.tags

                # Check for 'Name' property in tags object, if it doesn't exist, use the default
                instance_name = tags['Name'] if 'Name' in tags else 'Default EC2 Instance Name'

                # Print instance information
                print 'Instance Name:', instance_name, ' Instance Id:', instance.id, ' State:', instance.state,\
                    ' Launch Time:', instance.launch_time, ' IP address:', instance.private_ip_address,\
                    ' Private IP address:', instance.ip_address

    @staticmethod
    def create_instance(conn):
        """ Create a new instance """

        conn.run_instances("ami-c6972fb5", key_name="rsd_raul_cit_aws_key", instance_type="t2.micro")

    @staticmethod
    def create_instance_with_ami(conn, ami):
        """ Create a new instance based on AMI"""

        conn.run_instances(ami, key_name="rsd_raul_cit_aws_key", instance_type="t2.micro")

    @staticmethod
    def create_instance_with_so(conn, so):
        """ Create a new instance based on AMI"""

        # Select the AMI corresponding with Windows or Linux depending on the user
        ami = "ami-c6972fb5" if so == "windows" else "ami-f95ef58a"

        conn.run_instances(ami, key_name="rsd_raul_cit_aws_key", instance_type="t2.micro")

    @staticmethod
    def start_instance(conn, instance_id):
        """ Starts a stopped instance """

        conn.start_instances(instance_id, False)

    @staticmethod
    def stop_instances(conn):
        """ Stops all running instances"""

        # From all the running instances, extract the id and make a list
        instances_ids = [instance.id for instance in EC2Instance.find_instances_running(conn)]

        for instance_id in instances_ids:
            print "Stopping instance with id:", instance_id

        # Stop all the running instances
        conn.stop_instances(instances_ids, False)

    @staticmethod
    def stop_instance(conn, instance_id):
        """ Stops a running instance"""

        try:
            stopped = conn.stop_instances(instance_id, False)

            for instance in stopped:
                print "Stopping instance with id:", instance.id
        except exception.EC2ResponseError:
            print "Incorrect id format"

    @staticmethod
    def terminate_instance(conn, instance_id):
        """ Terminate a running or stopped instance"""

        conn.terminate_instances(instance_id)

    @staticmethod
    def terminate_all_instances(conn):
        """ Terminate all instances"""

        not_terminated = []
        for reservation in conn.get_all_instances():
            for inst in reservation.instances:
                print inst.id, inst.state, inst.public_dns_name
                if inst.state != u'terminated':
                    not_terminated.append(inst.id)

        if len(not_terminated) > 0:
            print "\nTerminating instances ", not_terminated
            conn.terminate_instances(instance_ids=not_terminated)
        else:
            print "Nothing to terminate"