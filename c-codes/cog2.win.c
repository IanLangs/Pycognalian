#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int returncode;
    char* stdout_output;
} SubprocessResult;

SubprocessResult subprocess_run(const char* command) {
    SECURITY_ATTRIBUTES saAttr = {sizeof(SECURITY_ATTRIBUTES), NULL, TRUE};
    HANDLE hStdOutRead, hStdOutWrite;
    if (!CreatePipe(&hStdOutRead, &hStdOutWrite, &saAttr, 0)) {
        perror("CreatePipe");
        exit(1);
    }
    SetHandleInformation(hStdOutRead, HANDLE_FLAG_INHERIT, 0);

    PROCESS_INFORMATION piProcInfo;
    STARTUPINFO siStartInfo;
    ZeroMemory(&piProcInfo, sizeof(PROCESS_INFORMATION));
    ZeroMemory(&siStartInfo, sizeof(STARTUPINFO));
    siStartInfo.cb = sizeof(STARTUPINFO);
    siStartInfo.hStdError = hStdOutWrite;
    siStartInfo.hStdOutput = hStdOutWrite;
    siStartInfo.dwFlags |= STARTF_USESTDHANDLES;

    char cmdline[1024];
    snprintf(cmdline, sizeof(cmdline), "cmd.exe /C %s", command);

    if (!CreateProcess(NULL, cmdline, NULL, NULL, TRUE, 0, NULL, NULL, &siStartInfo, &piProcInfo)) {
        perror("CreateProcess");
        exit(1);
    }

    CloseHandle(hStdOutWrite);

    char buffer[128];
    DWORD bytesRead;
    size_t size = 0;
    char* output = NULL;

    while (ReadFile(hStdOutRead, buffer, sizeof(buffer) - 1, &bytesRead, NULL) && bytesRead > 0) {
        buffer[bytesRead] = '\0';
        printf("%s", buffer); // salida en tiempo real

        char* tmp = realloc(output, size + bytesRead + 1);
        if (!tmp) { free(output); output = NULL; break; }
        output = tmp;
        memcpy(output + size, buffer, bytesRead + 1);
        size += bytesRead;
        output[size] = '\0';
    }

    WaitForSingleObject(piProcInfo.hProcess, INFINITE);
    DWORD exitCode;
    GetExitCodeProcess(piProcInfo.hProcess, &exitCode);

    CloseHandle(piProcInfo.hProcess);
    CloseHandle(piProcInfo.hThread);
    CloseHandle(hStdOutRead);

    SubprocessResult result;
    result.returncode = (int)exitCode;
    result.stdout_output = output;
    return result;
}

char* join(char** strings, int count, const char* sep) {
    if (count == 0) return strdup(""); // si no hay strings, retorno vacío

    size_t sep_len = strlen(sep);
    size_t total_len = 0;

    // Calculamos la longitud total del resultado
    for (int i = 0; i < count; i++) {
        total_len += strlen(strings[i]);
        if (i < count - 1) total_len += sep_len;
    }

    char* result = malloc(total_len + 1); // +1 para '\0'
    if (!result) return NULL;

    result[0] = '\0'; // inicializamos

    for (int i = 0; i < count; i++) {
        strcat(result, strings[i]);
        if (i < count - 1) strcat(result, sep);
    }

    return result;
}

int main(int argc, char *argv[]) {
    char cmd[1024];

    if (argc >= 2) {
        cmd[0] = '\0';

        strcat(cmd, "python cog2.py"); // comando base

        // agregamos todos los argumentos separados por espacio
        for (int i = 1; i < argc; i++) {
            strcat(cmd, " ");       // separador
            strcat(cmd, argv[i]);   // argumento
        }

        subprocess_run(cmd);

    } else {
        subprocess_run("python cog2.py a a a a a a a a a"); // cantidad de args incorrecta
    }

    return 0;
}
