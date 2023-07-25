FROM mcr.microsoft.com/dotnet/sdk:7.0@sha256:24f22e1142432dea3a34d350686be77be5e454ccb9fab7c00d67cd03c6e000a6 as build
WORKDIR /source

# copy csproj and restore as distinct layers
COPY ClutterbotWebApp/*.csproj .
RUN dotnet restore --use-current-runtime /p:PublishReadyToRun=true

# copy and publish app and libraries
COPY ClutterbotWebApp/. .
RUN dotnet publish --use-current-runtime --self-contained true --no-restore --output /app

# final stage/image
FROM mcr.microsoft.com/dotnet/aspnet:7.0@sha256:b30456a5d899c34443df908982f82ffb574412c848f30701b87ebddfe75e0571
WORKDIR /app
COPY --from=build /app .
ENTRYPOINT ["./ClutterbotWebApp"]
EXPOSE 80

# TODO: enable HTTPS
# https://stackoverflow.com/a/57109712/6480362
# ENV ASPNETCORE_HTTPS_PORT=7146
# ENV ASPNETCORE_URLS=https://+;http://+
# RUN dotnet dev-certs https

# https://docs.github.com/en/packages/learn-github-packages/connecting-a-repository-to-a-package#connecting-a-repository-to-a-container-image-using-the-command-line
LABEL org.opencontainers.image.source=https://github.com/4x0v7/clutterbot-devsecops-exercise
