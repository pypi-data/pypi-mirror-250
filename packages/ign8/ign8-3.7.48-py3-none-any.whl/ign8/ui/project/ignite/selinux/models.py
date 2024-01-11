from django.db import models

class Selinux(models.Model):
    hostname = models.CharField(max_length=128, primary_key=True)
    status = models.CharField(max_length=50)
    mount = models.CharField(max_length=50)
    rootdir = models.CharField(max_length=50)
    policyname = models.CharField(max_length=50)
    current_mode = models.CharField(max_length=50)
    configured_mode = models.CharField(max_length=50)
    mslstatus = models.CharField(max_length=50)
    memprotect = models.CharField(max_length=50)
    maxkernel = models.CharField(max_length=50)
    total = models.CharField(max_length=50)
    success = models.CharField(max_length=50)
    failed = models.CharField(max_length=50)
    sealerts = models.CharField(max_length=50)
    def __str__(self):
        return self.hostname
    
    class Meta:
        db_table = 'selinux'
        verbose_name = 'Selinux'
        verbose_name_plural = 'Selinux'
        ordering = ['hostname']
# the id must auto increment, otherwise the data will be overwritten


class SElinuxEvent(models.Model):
    digest = models.CharField(max_length=256, primary_key=True)
    hostname = models.CharField(max_length=128)
    event = models.CharField(max_length=1024)
    date = models.DateField()
    time = models.TimeField()
    serial_num = models.IntegerField()
    event_kind = models.CharField(max_length=256, blank=True, null=True)
    session = models.CharField(max_length=256, blank=True, null=True)
    subj_prime = models.CharField(max_length=256, blank=True, null=True)
    subj_sec = models.CharField(max_length=256, blank=True, null=True)
    subj_kind = models.CharField(max_length=256, blank=True, null=True)
    action = models.CharField(max_length=256, blank=True, null=True)
    result = models.CharField(max_length=256, blank=True, null=True)
    obj_prime = models.CharField(max_length=256, blank=True, null=True)
    obj_sec = models.CharField(max_length=256, blank=True, null=True)
    obj_kind = models.CharField(max_length=256, blank=True, null=True)
    how = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.digest
    
    class Meta:
        db_table = 'selinux_event'
        verbose_name = 'SElinuxEvent'
        verbose_name_plural = 'SElinuxEvent'
        ordering = ['date', 'time', 'hostname']



class SetroubleshootEntry(models.Model):
    cursor = models.CharField(max_length=255, primary_key=True)
    realtime_timestamp = models.BigIntegerField()
    monotonic_timestamp = models.BigIntegerField()
    boot_id = models.CharField(max_length=255)
    priority = models.IntegerField()
    syslog_facility = models.IntegerField()
    syslog_identifier = models.CharField(max_length=255)
    transport = models.CharField(max_length=255)
    pid = models.IntegerField()
    uid = models.IntegerField()
    gid = models.IntegerField()
    comm = models.CharField(max_length=255)
    exe = models.CharField(max_length=255)
    cmdline = models.TextField()
    cap_effective = models.BigIntegerField()
    selinux_context = models.CharField(max_length=255)
    systemd_cgroup = models.CharField(max_length=255)
    systemd_unit = models.CharField(max_length=255)
    systemd_slice = models.CharField(max_length=255)
    machine_id = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255)
    code_file = models.CharField(max_length=255)
    code_line = models.IntegerField()
    code_func = models.CharField(max_length=255)
    message_id = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    message = models.TextField()
    invocation_id = models.CharField(max_length=255)
    source_realtime_timestamp = models.BigIntegerField()

    def __str__(self):
        return f"SetroubleshootEntry - {self.cursor}"

    class Meta:
        verbose_name = 'Setroubleshoot Entry'
        verbose_name_plural = 'Setroubleshoot Entries'
