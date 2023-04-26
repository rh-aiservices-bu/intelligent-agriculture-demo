FROM registry.access.redhat.com/ubi9/python-39:latest


# Update base image for latest security updates
# (ubi images are not released that often)
USER 0
RUN dnf -y --setopt=tsflags=nodocs update && \
    dnf -y clean all --enablerepo='*'

USER 1001

# Install micropipenv to deploy packages from Pipfile.lock
RUN pip install -U "micropipenv[toml]"

WORKDIR /opt/app-root/src

# Copy files
COPY Pipfile.lock app.py ./

# Install packages and cleanup
# (all commands are chained to minimize layer size)
RUN echo "Installing softwares and packages" && \
    # Install Python packages \
    micropipenv install && \
    rm -f ./Pipfile.lock && \
    # Fix permissions to support pip in Openshift environments \
    chmod -R g+w /opt/app-root/lib/python3.9/site-packages && \
    fix-permissions /opt/app-root -P 

EXPOSE 5000

CMD ["python", "app.py"]