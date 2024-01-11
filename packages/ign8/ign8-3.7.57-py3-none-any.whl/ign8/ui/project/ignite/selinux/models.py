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
    __CURSOR = models.CharField(max_length=255, primary_key=True)
    __REALTIME_TIMESTAMP = models.BigIntegerField()
    __MONOTONIC_TIMESTAMP = models.BigIntegerField()
    _BOOT_ID = models.CharField(max_length=255)
    PRIORITY = models.IntegerField()
    SYSLOG_FACILITY = models.IntegerField()
    SYSLOG_IDENTIFIER = models.CharField(max_length=255)
    _TRANSPORT = models.CharField(max_length=255)
    _PID = models.IntegerField()
    _UID = models.IntegerField()
    _GID = models.IntegerField()
    _COMM = models.CharField(max_length=255)
    _EXE = models.CharField(max_length=255)
    _CMDLINE = models.TextField()
    _CAP_EFFECTIVE = models.CharField(max_length=255)
    _SELINUX_CONTEXT = models.CharField(max_length=255)
    _SYSTEMD_CGROUP = models.CharField(max_length=255)
    _SYSTEMD_UNIT = models.CharField(max_length=255)
    _SYSTEMD_SLICE = models.CharField(max_length=255)
    _MACHINE_ID = models.CharField(max_length=255)
    _HOSTNAME = models.CharField(max_length=255)
    CODE_FILE = models.CharField(max_length=255)
    CODE_LINE = models.IntegerField()
    CODE_FUNC = models.CharField(max_length=255)
    MESSAGE_ID = models.CharField(max_length=255)
    UNIT = models.CharField(max_length=255)
    MESSAGE = models.TextField()
    INVOCATION_ID = models.CharField(max_length=255)
    _SOURCE_REALTIME_TIMESTAMP = models.BigIntegerField()

    def __str__(self):
        return f"SetroubleshootEntry - {self.MESSAGE_ID}"

    class Meta:
        verbose_name = 'Setroubleshoot Entry'
        verbose_name_plural = 'Setroubleshoot Entries'
